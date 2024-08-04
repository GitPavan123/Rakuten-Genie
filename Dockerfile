# Use the official Python 3.10 slim image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the Python dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project source code to the working directory
COPY . .

# Expose the port that your application listens on (if applicable)
# EXPOSE 8000

# Define the command to run when the container starts
CMD ["python", "rakutengenie/main.py"]