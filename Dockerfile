# Base Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first, to leverage Docker's layer caching
COPY requirements.txt .

# Install dependencies without using cache to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Copy Logstash configuration into the container
COPY logstash/logstash.conf /usr/share/logstash/pipeline/logstash.conf

# Default command to run your application
CMD ["python", "-m", "server.server"]
