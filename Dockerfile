# Use an official Python runtime as a parent image
FROM python:3.13-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy dependency files
COPY Pipfile Pipfile.lock /app/

# Install pipenv and dependencies
RUN pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

# Copy the FastAPI app code into the container
COPY . /app

# Expose the port FastAPI will run on
EXPOSE 5000

# Command to run the FastAPI app
CMD ["uvicorn", "app.src.main:app", "--host", "0.0.0.0", "--port", "5000"]