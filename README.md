# Remote Wake-on-LAN

This project provides a simple web interface to wake up computers on your local network remotely using Tailscale.

## Prerequisites

- Python 3.8 or higher
- Tailscale installed and configured on both the server and client machines
- Wake-on-LAN enabled on the target computer

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your configuration:
   ```
   TARGET_MAC=XX:XX:XX:XX:XX:XX
   AUTH_USERNAME=your_username
   AUTH_PASSWORD=your_password
   ```

3. Run the server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Usage

1. Access the web interface at `http://nostromo.your-tailnet.ts.net:8000` from any device on your Tailscale network
2. Enter the configured username and password
3. Click the "Wake" button to send the magic packet

## Security Notes

- All traffic is encrypted through Tailscale
- Basic authentication is required to access the wake interface
- Store your `.env` file securely and never commit it to version control
