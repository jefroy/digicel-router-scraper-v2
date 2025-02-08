# Digicel Router Port Forward Scraper

An automated tool to monitor and extract port forwarding configurations from a Digicel router's web interface. The tool saves the configurations in both JSON and CSV formats and automatically generates RDP connection files when applicable.

## Features

- Automated monitoring of router port forwarding configurations
- Filtering for manual port forward entries
- Export to JSON and CSV formats
- Automatic RDP configuration file generation
- Docker support for easy deployment
- Comprehensive logging
- Configurable refresh intervals

## Prerequisites

- Docker and Docker Compose
- Access to a Digicel router on the local network
- Router admin credentials

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/digicel-router-scraper.git
cd digicel-router-scraper
```

2. Create and configure your environment file:
```bash
cp .env.example .env
nano .env  # Edit with your Supabase credentials and other settings
```

3. Create required directories and set permissions:
```bash
mkdir -p logs data
chmod -R 777 logs data
```

4. Build and start the container:
```bash
docker-compose up -d
```

### Alternative: Using Installation Script

For easier setup, you can use the provided installation script:
```bash
chmod +x install.sh
./install.sh
```

## Usage

### Running with Docker (Recommended)

1. Build and start the container:
```bash
docker-compose up -d
```

2. View logs:
```bash
docker-compose logs -f
```

3. Stop the container:
```bash
docker-compose down
```

### Running Locally

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the script:
```bash
python -m app.main
```

### Monitoring Logs

View logs in real-time:
```bash
docker-compose logs -f
```

Or check the log file directly:
```bash
tail -f logs/app.log
```

### Managing the Container

Start the container:
```bash
docker-compose up -d
```

Stop the container:
```bash
docker-compose down
```

Restart the container:
```bash
docker-compose restart
```

### Portainer Integration

The container will automatically appear in your Portainer dashboard. You can:
- Monitor container status
- View logs in real-time
- Manage container lifecycle (start/stop/restart)
- Check resource usage


## Configuration

The following environment variables can be configured in the .env file:

- `ROUTER_URL`: URL of the router's port forwarding page
- `ROUTER_USERNAME`: Router admin username
- `ROUTER_PASSWORD`: Router admin password
- `DUMP_PATH`: Path where output files will be saved
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)
- `REFRESH_INTERVAL`: Time between checks in seconds

## Output

The script generates the following files in the configured output directory:

- `ports.json`: JSON format of all manual port forwards
- `ports.csv`: CSV format of all manual port forwards
- `{hostname}.rdp`: RDP connection file (if RDP port forward is found)

## Logging

Logs are written to:
- Console output
- `logs/app.log` file

## Development

### Project Structure

```
digicel-router-scraper/
├── app/
│   ├── main.py           # Main application entry point
│   ├── utils/            # Utility modules
│   └── models/           # Data models
├── tests/                # Test cases
├── data/                 # Output directory
├── logs/                 # Log files
└── docker/               # Docker related files
```

### Running Tests

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is intended for personal use and monitoring of your own router. Please ensure you have proper authorization before using it on any network.