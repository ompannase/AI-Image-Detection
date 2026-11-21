import os
import numpy as np
import cv2
from tensorflow.keras.preprocessing.image import img_to_array

# Paths
input_folders = {"real": "archive/real", "fake": "archive/fake"}
output_folder = "dataset/processed"
os.makedirs(output_folder, exist_ok=True)

# Allowed image extensions
allowed_extensions = {".jpg", ".jpeg", ".png"}

# Process each category
for category, input_folder in input_folders.items():
    category_output_path = os.path.join(output_folder, category)
    os.makedirs(category_output_path, exist_ok=True)

    for img_name in os.listdir(input_folder):
        img_path = os.path.join(input_folder, img_name)

        # Check file extension
        if not any(img_name.lower().endswith(ext) for ext in allowed_extensions):
            print(f"Skipping {img_name}, unsupported format.")
            continue

        # Read image
        img = cv2.imread(img_path)
        if img is None:
            print(f"Skipping {img_name}, could not read file.")
            continue

        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Resize
        img = cv2.resize(img, (512, 512))

        # Convert to array
        img_array = img_to_array(img)

        # Save processed image
        save_path = os.path.join(category_output_path, img_name)
        cv2.imwrite(save_path, img_array.astype(np.uint8))  # Ensure proper format

print("✅ Processing complete. Images are resized!")
