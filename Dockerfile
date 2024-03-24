FROM python:3.11-buster

# RUN pip install poetry

COPY . .

# RUN poetry install

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install gunicorn

EXPOSE 80

ENV PORT 8080

# CMD ["bash", "-c", "gunicorn --bind 0.0.0.0:${PORT//\\/} app:app"]

# Copy the start script into the container
COPY start.sh /usr/src/app/start.sh

# Make the start script executable
RUN chmod +x /usr/src/app/start.sh

# Run the start script with bash when the container launches
CMD ["bash", "/usr/src/app/start.sh"]