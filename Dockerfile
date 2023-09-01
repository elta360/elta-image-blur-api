#FROM python:3.11.4
#RUN apt-get update && apt-get install -y libgl1-mesa-glx
#RUN apt-get install -y libopencv-dev python3-opencv
#RUN mkdir /app
#COPY . /app
#WORKDIR /app
#ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
#RUN pip3 install poetry
#RUN poetry install
#CMD ["poetry", "run", "python", "app.py"]


FROM python:3.11.4

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.5

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code