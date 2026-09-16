FROM python:3.10-slim

# Install system dependencies required by OpenCV (for libGL.so.1)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port used by FastAPI (now set to 60001)
EXPOSE 60001

# Run the FastAPI server using Uvicorn on port 60001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "60001"]



