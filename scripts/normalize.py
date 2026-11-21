import tensorflow as tf
import os

# Folder paths
input_real_folder = "dataset/resized/real"
input_fake_folder = "dataset/resized/fake"
output_folder = "dataset/normalized"

# Ensure output directories exist
os.makedirs(os.path.join(output_folder, "real"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "fake"), exist_ok=True)

def preprocess_and_save_image(image_path, output_subfolder):
    img = tf.io.read_file(image_path)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)  # Normalize to [0,1]

    # Get filename
    filename = os.path.basename(image_path)
    output_path = os.path.join(output_subfolder, filename)

    # Save normalized image (convert back to uint8 for saving)
    img = tf.image.convert_image_dtype(img, tf.uint8)
    tf.keras.utils.save_img(output_path, img.numpy())

# Process all images
for category in ["real", "fake"]:
    input_folder = os.path.join("dataset", "resized", category)
    output_subfolder = os.path.join(output_folder, category)
    os.makedirs(output_subfolder, exist_ok=True)

    for img_file in os.listdir(input_folder):
        img_path = os.path.join(input_folder, img_file)
        preprocess_and_save_image(img_path, output_subfolder)

print("✅ All images processed and saved in 'dataset/normalized'!")
