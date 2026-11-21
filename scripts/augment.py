import tensorflow as tf
import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from tqdm import tqdm  # For progress bar

# Paths
input_folder = "dataset/normalized"  # Path to normalized images
output_folder = "dataset/augmented"  # Path where augmented images will be saved
categories = ["real", "fake"]  # Categories

# Ensure output directories exist
for category in categories:
    os.makedirs(os.path.join(output_folder, category), exist_ok=True)

# Define augmentation settings with fixed seed
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    brightness_range=[0.8, 1.2],
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest"
)
seed = 42  # Reproducibility

# Number of augmented images per original image
num_augmented = 5  

# Process images in both categories
for category in categories:
    category_input_path = os.path.join(input_folder, category)
    category_output_path = os.path.join(output_folder, category)
    
    for img_name in tqdm(os.listdir(category_input_path), desc=f"Augmenting '{category}'"):
        img_path = os.path.join(category_input_path, img_name)

        try:
            # Load image and optionally resize to match model input size (e.g., 380x380)
            img = load_img(img_path, target_size=(380, 380))  
            img_array = img_to_array(img)  
            img_array = np.expand_dims(img_array, axis=0)  

            # Generate augmented images
            aug_iter = datagen.flow(img_array, batch_size=1, seed=seed)

            for i in range(num_augmented):
                aug_img = next(aug_iter)[0].astype("uint8")

                # Save augmented image
                aug_img_path = os.path.join(category_output_path, f"aug_{i}_{img_name}")
                tf.keras.utils.save_img(aug_img_path, aug_img)
        
        except Exception as e:
            print(f"⚠️ Error processing {img_name}: {e}")

print("✅ Augmentation completed. Images saved in 'dataset/augmented'!")
