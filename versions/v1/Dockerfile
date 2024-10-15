# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

COPY . .

#Install the required packages using pip3
RUN apt-get update && apt-get install -y python3-pip iputils-ping && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Expose port 80
EXPOSE 80

# Run the application
CMD ["python", "app.py"]
