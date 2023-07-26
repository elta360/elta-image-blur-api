import numpy as np
import cv2
import requests

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