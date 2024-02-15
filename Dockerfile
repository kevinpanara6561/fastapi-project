# Use the Python 3.11 base image from Amazon ECR Public Gallery
FROM public.ecr.aws/docker/library/python:3.11

# Copy the requirements file and install dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copy the Alembic configuration file
COPY ./alembic.ini /

# Create a directory for the application code
RUN mkdir /app
# Copy the application code into the container
COPY ./app/ /app/

# Expose port 8000 (Note: This is for documentation purposes, actual port binding is done when running the container)
EXPOSE 8000

# Set the working directory to /app
WORKDIR /app

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
