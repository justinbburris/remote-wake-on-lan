# Deployment Guide

This guide covers the deployment of the Remote Wake-on-LAN application using Docker.

## Prerequisites

1. **System Requirements**
   - Docker installed on the host system
   - Docker Compose installed on the host system
   - Wake-on-LAN enabled on the target machine
   - Tailscale installed and configured on the host system

2. **Network Requirements**
   - Host machine must be on the same local network as the target computer
   - Host machine must be part of your Tailscale network
   - Port 8000 must be available on the host

## Configuration

1. **Environment Variables**
   Create a `.env` file in the project directory with the following variables:
   ```
   TARGET_MAC=XX:XX:XX:XX:XX:XX    # MAC address of the target computer
   AUTH_USERNAME=your_username      # Username for web interface
   AUTH_PASSWORD=your_password      # Password for web interface
   ```

2. **File Structure**
   Ensure you have the following files in your project directory:
   ```
   .
   ├── .env
   ├── .dockerignore
   ├── docker-compose.yml
   ├── Dockerfile
   ├── main.py
   └── requirements.txt
   ```

## Deployment Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd remote-wake-on-lan
   ```

2. **Configure Environment**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit the environment file with your settings
   nano .env
   ```

3. **Build and Start the Container**
   ```bash
   # Build and start in detached mode
   docker-compose up -d

   # Verify the container is running
   docker-compose ps
   ```

4. **Check Logs**
   ```bash
   # View container logs
   docker-compose logs -f
   ```

## Accessing the Application

1. **Local Access**
   - Open `http://localhost:8000` in your web browser
   - Enter the configured username and password

2. **Remote Access**
   - Open `http://nostromo.your-tailnet.ts.net:8000` in your web browser
   - Enter the configured username and password

## Maintenance

1. **Updating the Application**
   ```bash
   # Pull latest changes
   git pull

   # Rebuild and restart the container
   docker-compose up -d --build
   ```

2. **Stopping the Application**
   ```bash
   # Stop the container
   docker-compose down
   ```

3. **Viewing Logs**
   ```bash
   # View all logs
   docker-compose logs

   # Follow logs in real-time
   docker-compose logs -f
   ```

## Troubleshooting

1. **Container Won't Start**
   - Check Docker logs: `docker-compose logs`
   - Verify environment variables are set correctly
   - Ensure port 8000 is not in use

2. **Wake-on-LAN Not Working**
   - Verify network mode is set to "host" in docker-compose.yml
   - Check if target MAC address is correct
   - Ensure target computer has Wake-on-LAN enabled

3. **Can't Access Web Interface**
   - Verify Tailscale connection
   - Check if container is running: `docker-compose ps`
   - Ensure port 8000 is accessible

## Security Considerations

1. **Environment Variables**
   - Keep `.env` file secure and never commit it to version control
   - Use strong passwords for authentication
   - Regularly rotate credentials

2. **Network Security**
   - All traffic is encrypted through Tailscale
   - Basic authentication is required for the web interface
   - Container runs as non-root user

3. **Updates**
   - Regularly update Docker images
   - Keep Tailscale client updated
   - Monitor for security advisories

## Backup and Recovery

1. **Backup Configuration**
   ```bash
   # Backup environment file
   cp .env .env.backup
   ```

2. **Recovery**
   ```bash
   # Restore from backup
   cp .env.backup .env

   # Rebuild and restart
   docker-compose up -d --build
   ```
