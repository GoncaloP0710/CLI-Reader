# Use an official Python runtime as a parent image
FROM python:3.13

# Set the working directory in the container
WORKDIR /app

# Copy the entire project into the container
COPY . /app

# Copy the requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH to include the project root
ENV PYTHONPATH=/app

# Set the entry point for the container
CMD ["python", "app/src/app.py"]