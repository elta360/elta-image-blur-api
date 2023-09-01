#Dockerfile for deployment to Heroku container with Poetry 1.5.1 and python 3.11.4

FROM python:3.11.4-slim-buster

# Install Poetry
RUN pip install poetry==1.5.1

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code/

# Expose port
EXPOSE 8000

# Run the application:
CMD ["poetry", "run", "python", "app.py"]