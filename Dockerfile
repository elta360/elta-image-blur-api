FROM python:3.11.4
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN apt-get install -y libopencv-dev python3-opencv-python
RUN mkdir /app
COPY . /app
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
CMD ["poetry", "run", "python", "app.py"]
