# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variable (ensure you handle this securely)
ENV OPENAI_API_KEY XXX

# Install Java Runtime Environment
RUN apt-get update && apt-get install -y \
    default-jdk \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire serverLLM directory into the container
COPY ./serverLLM /usr/src/app/serverLLM

# Set the working directory to the serverLLM directory
WORKDIR /usr/src/app/serverLLM

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Run server.py when the container launches
CMD ["python", "-u", "server.py"]
