# Installation Guide for Listening Machine

This guide covers how to install and configure the Remote Wake-on-LAN service on your listening machine server.

## Prerequisites

1. **System Requirements**
   - Docker installed on listening machine
   - Docker Compose installed on listening machine
   - Tailscale installed and configured on listening machine
   - Port 8000 available on listening machine

2. **Network Requirements**
   - listening machine must be on the same local network as the target computer
   - listening machine must be part of your Tailscale network

## Installation Steps

1. **Create Project Directory**
   ```bash
   mkdir -p ~/remote-wake-on-lan
   cd ~/remote-wake-on-lan
   ```

2. **Create Environment File**
   Create a `.env` file with your configuration:
   ```bash
   cat > .env << EOL
   TARGET_MAC=XX:XX:XX:XX:XX:XX    # MAC address of the computer to wake
   AUTH_USERNAME=admin             # Username for web interface
   AUTH_PASSWORD=your_password     # Password for web interface
   EOL
   ```

3. **Create Docker Compose File**
   Create a `docker-compose.yml` file:
   ```bash
   cat > docker-compose.yml << EOL
   version: '3.8'

   services:
     wake-on-lan:
       image: ghcr.io/your-username/remote-wake-on-lan:latest
       ports:
         - "8000:8000"
       environment:
         - TARGET_MAC=\${TARGET_MAC}
         - AUTH_USERNAME=\${AUTH_USERNAME}
         - AUTH_PASSWORD=\${AUTH_PASSWORD}
       restart: unless-stopped
       network_mode: "host"  # Required for Wake-on-LAN to work properly
   EOL
   ```

4. **Start the Service**
   ```bash
   docker compose up -d
   ```

5. **Verify Installation**
   ```bash
   # Check if container is running
   docker compose ps

   # View logs
   docker compose logs -f
   ```

## Automatic Startup

The service is configured to automatically restart on system reboot with `restart: unless-stopped` in the docker-compose file. However, to ensure Docker itself starts on boot:

1. **Enable Docker Service**
   ```bash
   sudo systemctl enable docker
   sudo systemctl enable docker-compose
   ```

2. **Verify Docker Auto-start**
   ```bash
   sudo systemctl status docker
   ```

## Updating the Service

To update to the latest version:

```bash
cd ~/remote-wake-on-lan
docker compose pull
docker compose up -d
```

## Accessing the Service

1. **Local Access**
   - Open `http://localhost:8000` in your web browser
   - Enter the configured username and password

2. **Remote Access**
   - Open `http://listening-machine.your-tailnet.ts.net:8000` in your web browser
   - Enter the configured username and password

## Troubleshooting

1. **Container Won't Start**
   ```bash
   # Check Docker logs
   docker-compose logs

   # Verify environment variables
   cat .env
   ```

2. **Wake-on-LAN Not Working**
   - Verify network mode is set to "host" in docker-compose.yml
   - Check if target MAC address is correct
   - Ensure target computer has Wake-on-LAN enabled

3. **Can't Access Web Interface**
   - Verify Tailscale connection
   - Check if container is running: `docker-compose ps`
   - Ensure port 8000 is accessible

## Security Notes

1. **Environment Variables**
   - Keep `.env` file secure
   - Use strong passwords
   - Regularly rotate credentials

2. **Network Security**
   - All traffic is encrypted through Tailscale
   - Basic authentication is required for the web interface
   - Container runs as non-root user

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
   docker-compose up -d
   ```
