# Use the official Python image from the Docker Hub
FROM python:3.9-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Multi-stage build to reduce the final image size
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy the application code from the builder stage
COPY --from=builder /app /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run app.py when the container launches
ENTRYPOINT ["uvicorn", "server:app"]
CMD ["--host", "0.0.0.0", "--port", "8000"]
