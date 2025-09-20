from PIL import Image, ImageFilter
import matplotlib.pyplot as plt
import os

def apply_blur_filter(image_path, output_path="blurred_image.png"):
    try: # open the image and apply a predefined blur function 
        img = Image.open(image_path)
        img_resized = img.resize((128, 128))
        img_blurred = img_resized.filter(ImageFilter.GaussianBlur(radius=2))

        # show image and save results
        plt.imshow(img_blurred)
        plt.axis('off')
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
        plt.close()
        print(f"Processed image saved as '{output_path}'.")

    # get processing errors
    except Exception as e:
        print(f"Error processing image: {e}")

# sepia helper
def apply_sepia(img):
    gray = img.convert("L")
    sepia = Image.merge("RGB", (
        gray.point(lambda p: int(p * 240 / 255)),
        gray.point(lambda p: int(p * 200 / 255)),
        gray.point(lambda p: int(p * 145 / 255))
    ))
    return sepia


def apply_sepia_filter(image_path, output_path="sepia_image.png"):
    try:
        img = Image.open(image_path)
        img_resized = img.resize((128, 128))
        img_sepia = apply_sepia(img_resized)

        # show image and save results
        plt.imshow(img_sepia)
        plt.axis('off')
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
        plt.close()
        print(f"Processed image saved as '{output_path}'.")

    except Exception as e:
        print(f"Error processing image: {e}")



# only runs if used directly in this implementation, 
# not used if imported into someone else's code
if __name__ == "__main__":
    print("Image Processor (type 'exit' to quit)\n")
    while True:
        image_path = input("Enter image filename (or 'exit' to quit): ").strip()
        if image_path.lower() == 'exit':
            print("Goodbye!")
            break
        if not os.path.isfile(image_path):
            print(f"File not found: {image_path}")
            continue

        # ask which filter to run
        choice = input("Type 1 for Blur, 2 for Sepia, 3 for Both: ").strip()
        base, ext = os.path.splitext(image_path)

        if choice == "1":
            output_file = f"{base}_blurred{ext}"
            apply_blur_filter(image_path, output_file)

        elif choice == "2":
            output_file = f"{base}_sepia{ext}"
            apply_sepia_filter(image_path, output_file)

        elif choice == "3":
            blurred_file = f"{base}_blurred{ext}"
            sepia_file = f"{base}_sepia{ext}"
            apply_blur_filter(image_path, blurred_file)
            apply_sepia_filter(image_path, sepia_file)

        else:
            print("Invalid choice. Please type 1, 2, or 3.")
