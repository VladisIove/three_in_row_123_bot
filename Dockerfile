# Use an official Python runtime as a parent image
FROM linuxserver/ffmpeg
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y ffmpeg && pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container (optional if your app runs on port 5000)
EXPOSE 5000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run backend.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
