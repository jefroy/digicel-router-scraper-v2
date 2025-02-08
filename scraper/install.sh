#!/bin/bash

# Colors for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

printf "${GREEN}Starting Digicel Router Port Forward Scraper installation...${NC}\n"

# Check if .env exists, if not create from example
if [ ! -f .env ]; then
    printf "${YELLOW}Creating .env file from example...${NC}\n"
    if [ -f .env.example ]; then
        cp .env.example .env
        printf "${YELLOW}Please edit .env file with your credentials:${NC}\n"
        echo "nano .env"
        exit 1
    else
        printf "${RED}Error: .env.example not found!${NC}\n"
        exit 1
    fi
fi

# Create required directories
printf "${YELLOW}Creating required directories...${NC}\n"
mkdir -p logs/digicel data
chmod -R 777 logs data

# Check if Docker is installed and running
if ! command -v docker &> /dev/null || ! docker info &> /dev/null; then
    printf "${RED}Docker is either not installed or not running properly.${NC}\n"
    printf "${YELLOW}Please ensure Docker is installed and the service is running.${NC}\n"
    printf "${YELLOW}You can install Docker using:${NC}\n"
    printf "curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh\n"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    printf "${RED}Docker Compose is not installed. Installing Docker Compose...${NC}\n"
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Build and start containers
printf "${YELLOW}Building and starting containers...${NC}\n"
docker-compose down
docker-compose up -d --build

# Check if containers are running
if [ $? -eq 0 ] && [ "$(docker ps -q -f name=digicel-port-scraper)" ]; then
    printf "${GREEN}Installation successful!${NC}\n"
    printf "Container is now running. You can view logs with:\n"
    printf "${YELLOW}docker-compose logs -f${NC}\n"
else
    printf "${RED}Error: Container failed to start. Please check logs:${NC}\n"
    docker-compose logs
    exit 1
fi