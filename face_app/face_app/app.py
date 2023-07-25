import numpy as np
import cv2
from flask import Flask, request, Response, jsonify
import requests

app = Flask(__name__)

haar_face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')

def read_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any HTTP error
        nparr = np.fromstring(response.content, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return image
    except requests.exceptions.RequestException as e:
        print("Error fetching the image:", e)
        return None

def convertToRGB(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def detect_faces(f_cascade, colored_img, scaleFactor=1.1):
    img_copy = np.copy(colored_img)
    # convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    # let's detect multiscale (some images may be closer to camera than others) images
    faces = f_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5);

    # go over list of faces and draw them as rectangles on original colored img
    for (x, y, w, h) in faces:
        cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    blur_faces(img_copy, faces)

    return img_copy

def blur_faces(image, faces):
    for (x, y, w, h) in faces:
        roi = image[y:y+h, x:x+w]
        # applying a gaussian blur over this new rectangle area
        roi = cv2.GaussianBlur(roi, (43, 43), 30)
        # impose this blurred image on original image to get final image
        image[y:y+roi.shape[0], x:x+roi.shape[1]] = roi

@app.route('/get_image', methods=['GET'])
def get_image():
    image_url = request.args.get('url')

    if image_url:
        image = read_image_from_url(image_url)
        if image is not None:
            _, img_encoded = cv2.imencode('.jpg', image)
            return Response(img_encoded.tobytes(), content_type='image/jpeg')
        else:
            return "Failed to read the image from the URL."
    else:
        return "Please provide the 'url' parameter with the image URL."

@app.route('/get_faces', methods=['GET'])
def get_faces():
    image_url = request.args.get('url')
    if image_url:
        image = read_image_from_url(image_url)
        if image is not None:
            faces_detected_img = detect_faces(haar_face_cascade, image)
            _, img_encoded = cv2.imencode('.jpg', faces_detected_img)
            return Response(img_encoded.tobytes(), content_type='image/jpeg')
        else:
            return "Failed to read the image from the URL."
    else:
        return "Please provide the 'url' parameter with the image URL."

if __name__ == '__main__':
    app.run()