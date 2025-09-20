# AI Image Processing and Classification Project

This project is designed to give you hands-on experience working with an image classifier and enhancing your programming skills using AI assistance. The project has two parts, each focused on different aspects of image classification and processing. By the end, you'll have explored fundamental concepts like Grad-CAM, image classification, and creative image filtering.

---------------------------------

# Paul Sachse
## (See Bottom For Final Report)

----------Begin Project---------- 

PART 1

3.3 Python Reflection - Base Classifier
While reviewing the explanations as someone who has never worked with python, the explanations were clear. Python appears very readable and syntactically does not seem to differ too much from C++. With this, I believe python will be a logical next language to understand and eventually master.

3.4 Top 3 Predictions
    1: bath_towel (0.23)
    2: bathtub (0.09)
    3: mongoose (0.06)

6 Analyze the Heatmap
When looking at my output, which I left as a side-by-side result rather than a single image with the heatmap overlay as a personal preference, the AI was clearly not able to distinguish one main subject. It seems to be drawn to the pattern on the blanket, but misses the main subject (dog) completely. In fact, the model seemed to miss the head of the subject almost entirely, indicating this model was not seeking out a living thing (or failed to), and was instead drawn to the busiest part of the image. 

---------------------------------

PART 2

1.3 Reflect on AI Explanation of Basic Filter
The AI's description of the filter code was easy to follow, despite being a novice python user. This was due, in part, to the fact that the code was already fairly short and readable. Still, being able to look at a block of code for the first time and read it like plain English is a testament to the language and explanations from artificial intelligence make learning the language along with best practices a delight. 

1.4 Blur Observations
The blur was easily applied with no additional work from the user and looks like a high quality gaussian blur from a professional editing application. I suspect part of this quick and easy processing is a result of resizing the image early in the process. The "amount" of blur could also be easily turned up or down by modifying the radius value of the gaussian blur effect. Overall, this seems to be a reliable and easy to use tool.

# Final Report

##### Heatmap Analysis
While working with this classifier and Grad-CAM utilizing the python language, I found this to be easy to adapt to with an extensive history in C++. When classifying the image, I noticed that the results were all presented with extremely low confidence: bath_towel (0.23), bathtub (0.09), mongoose (0.06), indicating the AI was not able to accurately describe the image. When looking at the side-by-side analysis, it seems that the model missed the actual subject completely, and its attention was instead drawn to the busiest part of the image, the blanket. This would further seem to indicate that this model does not seek out faces, but is looking for other clues to identify a subject. The model seemed to focus on the center of the image, and on the busiest parts, which is not a strong model for finding a subject.

##### Custom Filter Description
While implementing the image filtering, with some help from AI, I found python is an easy language to work with and is extremely readable. Taking a closer look at the gaussian blur, this effect came out looking high quality and could be used by professionals, especially if a higher resolution was maintained. This resizing, however, provides a faster filter application time and a better overall experience for the user. This blur was also easily customizable with the "radius" value. Furthermore, implementing a custom filter proved not to be too difficult using this toolset. To implement my sepia filter, I utilized the already developed Pillow grayscale method, and then implemented color tinting to the red, green, and blue values of the image to reach the desired effect. This retains the overall details of the image, but casts a classic look onto the image.

##### Experience Collaborating with AI
Working with AI to create this classifier and filter experience has enabled me to quickly complete a project, while learning about a language I've never used. I was able to quickly implement the heatmap with a quick block of code provided by ChatGPT. From there, the AI proceeded to explain exactly where the code should be placed, and once prompted, walked me through each line of the code. Still, some explanations were slightly too complicated and assumed prior knowledge, like understanding the use of "main" in this scenario, where it is only meant to be called when this program is run directly, and not when imported to another program. After a few clarifying prompts, the AI and I were able to get on the same page and continue working. Finally, when I would occasionally run into errors, a quick description of the error generally prompted a fix that could be implemented in seconds. Working with AI, I have adjusted to asking more questions and seeking out more explanations, rather than just trying to find a block of code that works. This was an excellent example of expedited development and learning with the assistance of AI.