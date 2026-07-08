# Use an official Python runtime as a parent image (slim version for smaller size)
FROM python:3.10-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirement.txt .

# Install any needed packages specified in requirement.txt
# --no-cache-dir helps keep the docker image size small
RUN pip install --no-cache-dir -r requirement.txt

# Copy the rest of the application code
COPY . .

# Expose port 5000 (the port Gunicorn will listen on)
EXPOSE 5000

# Command to run the application using Gunicorn
# -w 4 means 4 worker processes
# -b 0.0.0.0:5000 means bind to all interfaces on port 5000
# run:app means look in run.py for the 'app' variable
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
