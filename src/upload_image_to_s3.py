import boto3
import io
import cv2
import os
from dotenv import load_dotenv

load_dotenv()

aws_bucket_name = os.getenv("AWS_BUCKET_NAME")


def upload_image_to_s3(object_name, image):
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("REGION_NAME"),
        )

        _, buffer = cv2.imencode(".jpg", image)
        s3.upload_fileobj(io.BytesIO(buffer), aws_bucket_name, object_name)
        print("Image uploaded successfully to S3.")
    except Exception as e:
        print("Error uploading the image to S3:", e)
