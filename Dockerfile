# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY fan_control.py /app/

# Install necessary tools
RUN apt-get update && apt-get install -y \
    ipmitool \
    nvidia-smi && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install necessary Python libraries
RUN pip install nvidia-ml-py3

# Set the entrypoint to run the script
ENTRYPOINT ["python3", "fan_control.py"]
