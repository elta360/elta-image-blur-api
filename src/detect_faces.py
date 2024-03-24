import numpy as np
import cv2

haar_face_cascade = cv2.CascadeClassifier("data/haarcascade_frontalface_alt.xml")


def convertToRGB(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def detect_faces(f_cascade, colored_img, scaleFactor=1.1):
    img_copy = np.copy(colored_img)
    # convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    # let's detect multiscale (some images may be closer to camera than others) images
    faces = f_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5)

    # go over list of faces and draw them as rectangles on original colored img
    for x, y, w, h in faces:
        cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)

    blur_faces(img_copy, faces)

    return img_copy


def blur_faces(image, faces):
    for x, y, w, h in faces:
        roi = image[y : y + h, x : x + w]
        # applying a gaussian blur over this new rectangle area
        roi = cv2.GaussianBlur(roi, (43, 43), 30)
        # impose this blurred image on original image to get final image
        image[y : y + roi.shape[0], x : x + roi.shape[1]] = roi
