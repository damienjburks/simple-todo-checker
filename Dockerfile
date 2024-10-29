# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the action files into the Docker image
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

# Install any dependencies
RUN pip install -r requirements.txt

# Set the entrypoint to python, so args can run the main script
ENTRYPOINT ["python"]
