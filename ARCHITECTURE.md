# Remote Wake-on-LAN Architecture

## System Overview

This system enables remote Wake-on-LAN functionality through a secure web interface, leveraging Tailscale for secure remote access. The architecture consists of three main components:

1. **Web Server (nostromo)**
   - Runs on a machine that's always on within your local network
   - Hosts the FastAPI application
   - Has direct access to the local network for sending Wake-on-LAN packets

2. **Target Computer**
   - The machine you want to wake up remotely
   - Must have Wake-on-LAN enabled in BIOS/UEFI
   - Must be connected to the same local network as the server

3. **Client Device (e.g., phone)**
   - Any device with a web browser
   - Must be connected to your Tailscale network
   - Used to trigger the wake command

## Network Architecture

```
[Client Device] <---> [Tailscale Network] <---> [nostromo (Server)] <---> [Local Network] <---> [Target Computer]
```

- All communication between the client and server is encrypted through Tailscale
- The server must be able to send UDP broadcast packets on the local network
- The target computer must be configured to receive Wake-on-LAN packets

## Security Architecture

1. **Transport Layer Security**
   - All traffic is encrypted through Tailscale's WireGuard implementation
   - No need for additional SSL/TLS certificates

2. **Authentication**
   - Basic authentication using username/password
   - Credentials stored in environment variables
   - Secure credential comparison using `secrets.compare_digest()`

3. **Access Control**
   - Only devices on your Tailscale network can access the interface
   - Additional authentication required to send wake commands

## Common Use Cases

### 1. Remote Work Setup
- Wake your work computer before arriving at the office
- Access your home computer while traveling
- Wake servers or workstations in a remote office

### 2. Home Automation
- Wake your media server before streaming
- Start your gaming PC remotely
- Power up home lab equipment when needed

### 3. System Administration
- Wake servers for maintenance
- Power up backup systems
- Remote management of network devices

## Implementation Details

### Server Component
- FastAPI application running on port 8000
- Two main endpoints:
  - `GET /`: Web interface
  - `POST /wake`: Wake-on-LAN command endpoint
- Uses `wakeonlan` package to send magic packets

### Client Interface
- Simple, mobile-friendly web interface
- Single button to trigger wake command
- Visual feedback for success/failure
- Basic authentication prompt

## Configuration

The system requires three main configuration parameters:
1. `TARGET_MAC`: MAC address of the computer to wake
2. `AUTH_USERNAME`: Username for basic authentication
3. `AUTH_PASSWORD`: Password for basic authentication

## Limitations and Considerations

1. **Network Requirements**
   - Target computer must be connected to power
   - Wake-on-LAN must be enabled in BIOS/UEFI
   - Network interface must support Wake-on-LAN

2. **Security Considerations**
   - Keep authentication credentials secure
   - Regularly update Tailscale and Python packages
   - Monitor access logs for unauthorized attempts

3. **Reliability**
   - Wake-on-LAN packets are UDP broadcasts
   - Some networks may block UDP broadcasts
   - Multiple attempts may be needed in some cases

## Deployment

For detailed deployment instructions, including Docker setup and configuration, please refer to the [Deployment Guide](DEPLOYMENT.md).

## Troubleshooting

Common issues and solutions:

1. **Computer doesn't wake up**
   - Verify Wake-on-LAN is enabled in BIOS
   - Check MAC address is correct
   - Ensure network interface supports Wake-on-LAN
   - Try sending multiple wake packets

2. **Can't access the web interface**
   - Verify Tailscale connection
   - Check server is running
   - Confirm port 8000 is accessible
   - Verify authentication credentials

3. **Server errors**
   - Check server logs
   - Verify environment variables are set
   - Ensure Python dependencies are installed
   - Check network permissions for UDP broadcasts
