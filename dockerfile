# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Create and set the working directory
WORKDIR /app

# Copy the application files to the container
COPY . /app

#define argument to receive git sha id while the docker is run
ARG COMMIT_SHA

#store the git sha id into the file
RUN echo ${COMMIT_SHA} > commit_sha.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on Not Required for Functionality: The EXPOSE instruction does not actually open or map the port on  host machine; it’s just a way to document the port. The actual port mapping is done using the -p option when running the container or in Docker Compose.
EXPOSE $SERVICE_PORT

# Command to run the application
CMD ["python3", "RubyKInfoLog.py"]
