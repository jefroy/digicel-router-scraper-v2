#!/bin/bash

echo "Starting Digicel Router Port Forward Scraper installation..."

# Check if .env exists, if not create from example
if [ ! -f .env ]; then
    echo "Creating .env file from example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "Please edit .env file with your credentials:"
        echo "nano .env"
        exit 1
    else
        echo "Error: .env.example not found!"
        exit 1
    fi
fi

# Create required directories
echo "Creating required directories..."
mkdir -p logs data
chmod -R 777 logs data

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Build and start containers
echo "Building and starting containers..."
docker-compose down
docker-compose up -d --build

# Check if containers are running
if [ $? -eq 0 ]; then
    echo "Installation successful!"
    echo "Container is now running. You can view logs with:"
    echo "docker-compose logs -f"
else
    echo "Error: Container failed to start. Please check logs:"
    docker-compose logs
    exit 1
fi