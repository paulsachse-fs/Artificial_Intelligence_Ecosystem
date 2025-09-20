import tensorflow as tf
tf.get_logger().setLevel('ERROR')
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

# load model
model = MobileNetV2(weights="imagenet")

def classify_image(image_path):
    try: # load pictures and process for analysis
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        # get predictions from model
        predictions = model.predict(img_array)
        # convert results to output
        decoded_predictions = decode_predictions(predictions, top=3)[0]

        print("\nTop-3 Predictions for", image_path)
        for i, (_, label, score) in enumerate(decoded_predictions):
            print(f"  {i + 1}: {label} ({score:.2f})")

                    # ✅ Add Grad-CAM generation here
        gradcam_path = save_gradcam(
            image_path,
            model,
            last_conv_layer_name="Conv_1",
            out_path=None,
            alpha=0.45,
            class_index=None  # None = top predicted class
        )
        print(f"Grad-CAM saved to: {gradcam_path}")

    except Exception as e:
        print(f"Error processing '{image_path}': {e}")

# begin helpers for Grad-Cam
from tensorflow.keras.models import Model
from PIL import Image
import os

def _get_img_array_for_model(image_path, target_size=(224, 224)):
    img = image.load_img(image_path, target_size=target_size)
    arr = image.img_to_array(img)
    arr = preprocess_input(arr)
    arr = np.expand_dims(arr, axis=0)  # (1, H, W, 3)
    return arr

def make_gradcam_heatmap(img_array, model, last_conv_layer_name="Conv_1", class_index=None):
    """
    img_array: preprocessed array with shape (1, H, W, 3)
    model: a Keras model (e.g., MobileNetV2(weights='imagenet'))
    last_conv_layer_name: name of the last conv layer to use for Grad-CAM
    class_index: integer class idx to explain; if None, uses top predicted class
    """
    # Build a model mapping the input image to the activations of the last conv layer
    # and the model’s predictions.
    last_conv_layer = model.get_layer(last_conv_layer_name)
    grad_model = Model([model.inputs], [last_conv_layer.output, model.output])

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        if class_index is None:
            class_index = tf.argmax(predictions[0])
        class_channel = predictions[:, class_index]

    # Compute gradients of the top predicted class with respect to the conv features
    grads = tape.gradient(class_channel, conv_outputs)

    # Global-average-pool the gradients to get weight for each filter channel
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # Weight the conv outputs by the pooled grads (channel-wise)
    conv_outputs = conv_outputs[0]  # (Hc, Wc, C)
    heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)

    # Apply ReLU and normalize to [0, 1]
    heatmap = tf.nn.relu(heatmap)
    heatmap = heatmap / (tf.reduce_max(heatmap) + 1e-8)
    return heatmap.numpy()  # (Hc, Wc)

def save_gradcam(image_path, model, last_conv_layer_name="Conv_1", out_path=None, alpha=0.4, class_index=None):
    """
    Generates and saves a Grad-CAM overlay next to the original image.
    - out_path: if None, saves as <image_basename>_gradcam.jpg alongside the image.
    - alpha: overlay transparency [0..1]
    """
    # 1) Preprocess for the model
    img_array = _get_img_array_for_model(image_path, target_size=(224, 224))

    # 2) Build heatmap
    heatmap = make_gradcam_heatmap(img_array, model, last_conv_layer_name, class_index)

    # 3) Load original image (keep original size for nicer overlay)
    orig = Image.open(image_path).convert("RGB")
    w, h = orig.size

    # 4) Resize heatmap to original size
    heatmap_resized = Image.fromarray((heatmap * 255).astype("uint8")).resize((w, h), resample=Image.BILINEAR)

    # 5) Convert heatmap to RGB using a simple colormap (no external deps)
    # Create a colored heatmap by stacking: (R=heatmap, G=zeros, B=255-heatmap)
    hm = np.array(heatmap_resized, dtype=np.uint8)
    colored = np.stack([hm, np.zeros_like(hm), 255 - hm], axis=-1)  # shape (h, w, 3)
    colored_img = Image.fromarray(colored, mode="RGB")

    # 6) Overlay heatmap on original
    overlay = Image.blend(orig, colored_img, alpha=alpha)

    # 7) Create side-by-side (orig | overlay) for easy inspection
    combo = Image.new("RGB", (w * 2, h))
    combo.paste(orig, (0, 0))
    combo.paste(overlay, (w, 0))

    # 8) Save
    if out_path is None:
        root, ext = os.path.splitext(image_path)
        out_path = f"{root}_gradcam.jpg"
    combo.save(out_path, quality=95)
    return out_path
# end helpers for Grad-Cam

if __name__ == "__main__":
    print("Image Classifier (type 'exit' to quit)\n")
    while True:
        image_path = input("Enter image filename: ").strip()
        if image_path.lower() == "exit":
            print("Goodbye!")
            break
        classify_image(image_path)
