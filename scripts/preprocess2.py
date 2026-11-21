import os
import random
from PIL import Image
from pillow_heif import register_heif_opener
import tensorflow as tf
from tqdm import tqdm

# Register HEIC support
register_heif_opener()

# Set seed
random.seed(42)

# Paths
input_folder = "unsplash_portraits"
converted_folder = "unsplash_converted"
output_base = "new_dataset"
split_base = os.path.join(output_base, "split")

# Valid extensions after conversion
valid_extensions = [".jpg", ".jpeg", ".png"]

# Ensure necessary directories exist
os.makedirs(converted_folder, exist_ok=True)
for split in ["train", "val", "test"]:
    os.makedirs(os.path.join(split_base, split, "real"), exist_ok=True)

# --- Step 1: Convert HEIC and valid images ---
for file in os.listdir(input_folder):
    ext = os.path.splitext(file)[1].lower()
    input_path = os.path.join(input_folder, file)

    try:
        if ext == ".heic":
            img = Image.open(input_path).convert("RGB")
            output_name = os.path.splitext(file)[0] + ".jpg"
            img.save(os.path.join(converted_folder, output_name), "JPEG")
        elif ext in valid_extensions:
            img = Image.open(input_path).convert("RGB")
            img.save(os.path.join(converted_folder, file))
    except Exception as e:
        print(f"⚠️ Error converting {file}: {e}")

# --- Step 2: Gather all valid images ---
image_files = [
    f for f in os.listdir(converted_folder)
    if os.path.splitext(f)[1].lower() in valid_extensions
]
random.shuffle(image_files)

# --- Step 3: Split ---
total = len(image_files)
train_split = int(0.7 * total)
val_split = int(0.15 * total)

train_files = image_files[:train_split]
val_files = image_files[train_split:train_split + val_split]
test_files = image_files[train_split + val_split:]

# --- Step 4: Resize + Normalize + Save ---
def process_and_save(image_list, split_name):
    for filename in tqdm(image_list, desc=f"Processing {split_name}"):
        input_path = os.path.join(converted_folder, filename)
        output_path = os.path.join(split_base, split_name, "real", filename)

        try:
            img = tf.io.read_file(input_path)
            img = tf.image.decode_image(img, channels=3, expand_animations=False)
            img = tf.image.resize(img, [512, 512])
            img = tf.image.convert_image_dtype(img, tf.float32)
            img = tf.image.convert_image_dtype(img, tf.uint8)
            tf.keras.utils.save_img(output_path, img.numpy())
        except Exception as e:
            print(f"⚠️ Error processing {filename}: {e}")

# Process all splits
process_and_save(train_files, "train")
process_and_save(val_files, "val")
process_and_save(test_files, "test")

print("✅ Done! Converted, resized, normalized, and split real images saved in 'new_dataset/split/'")
