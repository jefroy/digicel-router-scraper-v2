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

# Check Docker version and status
docker_version=$(docker --version)
if [ $? -ne 0 ]; then
    echo "Error: Docker is not running or there are permission issues."
    echo "Please ensure Docker daemon is running and you have proper permissions."
    exit 1
fi
echo "Found Docker: $docker_version"

# Check Docker Compose installation and version
compose_version=$(docker-compose --version)
if [ $? -ne 0 ]; then
    echo "Error: Docker Compose is not working properly."
    echo "Try removing and reinstalling Docker Compose:"
    echo "sudo rm $(which docker-compose)"
    echo "sudo curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose"
    echo "sudo chmod +x /usr/local/bin/docker-compose"
    exit 1
fi
echo "Found Docker Compose: $compose_version"

# Stop any existing containers gracefully
echo "Stopping any existing containers..."
docker-compose down --remove-orphans || true

# Clean up any old containers and images
echo "Cleaning up old containers and images..."
docker rm -f digicel-port-scraper 2>/dev/null || true
docker rmi -f digicel-router-scraper-v2_scraper 2>/dev/null || true

# Build and start containers
echo "Building and starting containers..."
if ! docker-compose up -d --build; then
    echo "Error: Failed to build and start containers."
    echo "Checking Docker Compose logs:"
    docker-compose logs
    exit 1
fi

# Verify container is running
if [ "$(docker ps -q -f name=digicel-port-scraper)" ]; then
    echo "Installation successful!"
    echo "Container is now running. You can view logs with:"
    echo "docker-compose logs -f"
else
    echo "Error: Container failed to start. Please check logs:"
    docker-compose logs
    exit 1
fi