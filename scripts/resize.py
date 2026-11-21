import cv2
import os

# Paths
input_folder_fake = "archive/fake"
input_folder_real = "archive/real"
output_folder = "dataset/resized"

# Create output directories
os.makedirs(os.path.join(output_folder, "fake"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "real"), exist_ok=True)

# Function to resize images
def resize_images(input_folder, output_subfolder):
    for img_name in os.listdir(input_folder):
        img_path = os.path.join(input_folder, img_name)
        img = cv2.imread(img_path)
        if img is not None:
            resized_img = cv2.resize(img, (380, 380))
            cv2.imwrite(os.path.join(output_subfolder, img_name), resized_img)

# Process fake and real images
resize_images(input_folder_fake, os.path.join(output_folder, "fake"))
resize_images(input_folder_real, os.path.join(output_folder, "real"))

print("Resizing complete!")
