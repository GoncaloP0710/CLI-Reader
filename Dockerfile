# TODO: The images path dont work on docker and are different on docker vs venv... Correct that latter

# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container to /app/app
WORKDIR /app

# Copy the requirements and install dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Install required system libraries for terminal compatibility and image processing
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libtiff5-dev \
    libopenjp2-7-dev \
    libpng-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1 \
    ncurses-base \
    ncurses-term \
    locales && \
    locale-gen en_US.UTF-8

# Set the locale to UTF-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Copy the entire project into the container
COPY . /app

# Set PYTHONPATH to include the project root
ENV PYTHONPATH=/app

# Set the entry point for the container
CMD ["python", "app/src/app.py"]