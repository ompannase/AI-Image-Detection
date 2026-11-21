from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import cv2

app = Flask(__name__)
model = tf.keras.models.load_model("models/final_model.keras")

UPLOAD_FOLDER = "static/uploads/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def preprocess_image(img_path):
    # Load the image using OpenCV
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize to model input size
    img = cv2.resize(img, (380, 380))

    # ✅ Apply Gaussian blur
    img = cv2.GaussianBlur(img, (9, 9), 0)

    # Normalize to 0–1
    img = img.astype("float32") / 255.0

    # Add batch dimension
    img_array = np.expand_dims(img, axis=0)

    return img_array

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)

            img = preprocess_image(file_path)
            prediction = model.predict(img)[0][0]
            print(f"Raw model prediction: {prediction}")
            
            # Calculate confidence percentage
            if prediction > 0.5:
                result = "Real"
                confidence = prediction * 100  # Direct percentage for real
            else:
                result = "Fake"
                confidence = (1 - prediction) * 100  # Inverted percentage for fake
            
            return render_template(
                "index.html",
                filename=file.filename,
                result=result,
                confidence=confidence
            )

    return render_template("index.html", filename=None, result=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)