from flask import Flask, render_template, request
from ultralytics import YOLO
import os
import cv2

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# Load YOLO model
model = YOLO("/home/waqas-ahmad/Desktop/models/model/best.pt")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    if 'file' not in request.files:
        return "No file uploaded"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        file.filename
    )

    file.save(filepath)

    # Run detection
    results = model(filepath)

    # Save result image
    result_path = os.path.join(
        app.config['RESULT_FOLDER'],
        file.filename
    )

    annotated_frame = results[0].plot()

    cv2.imwrite(result_path, annotated_frame)

    return render_template(
        'index.html',
        uploaded_image=filepath,
        result_image=result_path
    )


if __name__ == '__main__':
    app.run(debug=True)