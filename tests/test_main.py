import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Set environment variables before importing the app
os.environ.update({
    'TARGET_MAC': '00:11:22:33:44:55',
    'AUTH_USERNAME': 'testuser',
    'AUTH_PASSWORD': 'testpass'
})

# Import the main module directly to fix the coverage warning
import remote_wake_on_lan.main
from remote_wake_on_lan.main import app

# Test client
client = TestClient(app)

def test_root_unauthorized():
    """Test that root endpoint requires authentication"""
    response = client.get("/")
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers

def test_root_authorized():
    """Test that root endpoint returns HTML when authorized"""
    response = client.get("/", auth=("testuser", "testpass"))
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Remote Wake-on-LAN" in response.text
    assert "Wake Computer" in response.text

def test_wake_unauthorized():
    """Test that wake endpoint requires authentication"""
    response = client.post("/wake")
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers

@patch('remote_wake_on_lan.main.send_magic_packet')
def test_wake_authorized(mock_send_magic_packet):
    """Test that wake endpoint sends magic packet when authorized"""
    mock_send_magic_packet.return_value = None  # Explicitly set return value
    response = client.post("/wake", auth=("testuser", "testpass"))
    assert response.status_code == 200
    assert response.json() == {"message": "Wake-on-LAN packet sent successfully"}
    mock_send_magic_packet.assert_called_once_with("00:11:22:33:44:55")

@patch('remote_wake_on_lan.main.send_magic_packet')
def test_wake_error_handling(mock_send_magic_packet):
    """Test error handling when sending magic packet fails"""
    mock_send_magic_packet.side_effect = Exception("Test error")
    response = client.post("/wake", auth=("testuser", "testpass"))
    assert response.status_code == 500
    assert "Failed to send wake packet" in response.json()["detail"]

def test_invalid_credentials():
    """Test that invalid credentials are rejected"""
    response = client.get("/", auth=("wronguser", "wrongpass"))
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers

def test_missing_mac_address():
    """Test handling of missing MAC address configuration"""
    with patch.dict(os.environ, {'TARGET_MAC': ''}, clear=True):
        response = client.post("/wake", auth=("testuser", "testpass"))
        assert response.status_code == 500
        assert "Target MAC address not configured" in response.json()["detail"]
