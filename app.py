import cv2
from flask import Flask, request, Response
from src.detect_faces import detect_faces, haar_face_cascade
from src.read_image import read_image_from_url

app = Flask(__name__)


@app.route("/get_faces", methods=["GET"])
def get_faces():
    image_url = request.args.get("url")
    if image_url:
        image = read_image_from_url(image_url)
        if image is not None:
            faces_detected_img = detect_faces(haar_face_cascade, image)
            _, img_encoded = cv2.imencode(".jpg", faces_detected_img)
            return Response(img_encoded.tobytes(), content_type="image/jpeg")
        else:
            return "Failed to read the image from the URL."
    else:
        return "Please provide the 'url' parameter with the image URL."


if __name__ == "__main__":
    app.run()
