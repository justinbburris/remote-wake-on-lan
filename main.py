from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from wakeonlan import send_magic_packet
import os
from dotenv import load_dotenv
import secrets

# Load environment variables
load_dotenv()

app = FastAPI(title="Remote Wake-on-LAN")
security = HTTPBasic()

# Configuration
TARGET_MAC = os.getenv("TARGET_MAC")
AUTH_USERNAME = os.getenv("AUTH_USERNAME")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, AUTH_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, AUTH_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials

@app.get("/", response_class=HTMLResponse)
async def root(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Remote Wake-on-LAN</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    text-align: center;
                }
                button {
                    background-color: #4CAF50;
                    border: none;
                    color: white;
                    padding: 15px 32px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    cursor: pointer;
                    border-radius: 4px;
                }
                button:hover {
                    background-color: #45a049;
                }
                #status {
                    margin-top: 20px;
                    padding: 10px;
                    border-radius: 4px;
                }
                .success {
                    background-color: #dff0d8;
                    color: #3c763d;
                }
                .error {
                    background-color: #f2dede;
                    color: #a94442;
                }
            </style>
        </head>
        <body>
            <h1>Remote Wake-on-LAN</h1>
            <button onclick="wakeComputer()">Wake Computer</button>
            <div id="status"></div>
            <script>
                async function wakeComputer() {
                    const statusDiv = document.getElementById('status');
                    try {
                        const response = await fetch('/wake', {
                            method: 'POST',
                            headers: {
                                'Authorization': 'Basic ' + btoa(window.location.href.split('//')[1].split('@')[0])
                            }
                        });
                        const data = await response.json();
                        statusDiv.textContent = data.message;
                        statusDiv.className = response.ok ? 'success' : 'error';
                    } catch (error) {
                        statusDiv.textContent = 'Error: ' + error.message;
                        statusDiv.className = 'error';
                    }
                }
            </script>
        </body>
    </html>
    """

@app.post("/wake")
async def wake_computer(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    if not TARGET_MAC:
        raise HTTPException(status_code=500, detail="Target MAC address not configured")

    try:
        send_magic_packet(TARGET_MAC)
        return {"message": "Wake-on-LAN packet sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send wake packet: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
