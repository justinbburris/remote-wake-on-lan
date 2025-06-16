#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install it first."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOL
TARGET_MAC=XX:XX:XX:XX:XX:XX    # Replace with your target computer's MAC address
AUTH_USERNAME=admin             # Your chosen username
AUTH_PASSWORD=your_password     # Your chosen password
SECRET_KEY=$(openssl rand -hex 32)  # This will generate a secure random key
EOL
    echo "Please edit .env file with your configuration before running the application."
    exit 1
fi

# Run the application
echo "Starting the application..."
uvicorn remote_wake_on_lan.main:app --host 0.0.0.0 --port 8000 --reload
