# digicel-scraper/install.sh
#!/bin/bash

# Colors for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Starting Digicel Router Port Forward Scraper installation...${NC}"

# Check if .env exists, if not create from example
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from example...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${YELLOW}Please edit .env file with your credentials:${NC}"
        echo "nano .env"
        exit 1
    else
        echo -e "${RED}Error: .env.example not found!${NC}"
        exit 1
    fi
fi

# Create required directories
echo -e "${YELLOW}Creating required directories...${NC}"
mkdir -p logs/digicel data
chmod -R 777 logs data

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Installing Docker...${NC}"
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed. Installing Docker Compose...${NC}"
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Build and start containers
echo -e "${YELLOW}Building and starting containers...${NC}"
docker-compose down
docker-compose up -d --build

# Check if containers are running
if [ $? -eq 0 ] && [ "$(docker ps -q -f name=digicel-port-scraper)" ]; then
    echo -e "${GREEN}Installation successful!${NC}"
    echo -e "Container is now running. You can view logs with:"
    echo -e "${YELLOW}docker-compose logs -f${NC}"
else
    echo -e "${RED}Error: Container failed to start. Please check logs:${NC}"
    docker-compose logs
    exit 1
fi
