import os
import shutil
import random

# Define paths
input_folder = "dataset/normalized"
output_folder = "dataset/split"
categories = ["real", "fake"]

# Split percentages
train_split = 0.8
val_split = 0.1
test_split = 0.1

# Ensure output directories exist
for split in ["train", "val", "test"]:
    for category in categories:
        os.makedirs(os.path.join(output_folder, split, category), exist_ok=True)

# Function to split and move images
def split_data(category):
    category_path = os.path.join(input_folder, category)
    images = os.listdir(category_path)
    random.shuffle(images)

    train_count = int(len(images) * train_split)
    val_count = int(len(images) * val_split)

    train_images = images[:train_count]
    val_images = images[train_count:train_count + val_count]
    test_images = images[train_count + val_count:]

    for img_name in train_images:
        shutil.move(os.path.join(category_path, img_name), os.path.join(output_folder, "train", category, img_name))
    for img_name in val_images:
        shutil.move(os.path.join(category_path, img_name), os.path.join(output_folder, "val", category, img_name))
    for img_name in test_images:
        shutil.move(os.path.join(category_path, img_name), os.path.join(output_folder, "test", category, img_name))

# Split each category
for category in categories:
    split_data(category)

print("✅ Dataset split completed successfully!")
