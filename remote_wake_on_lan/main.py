from fastapi import FastAPI, HTTPException, Request, Response, Form
from fastapi.responses import HTMLResponse
from wakeonlan import send_magic_packet
import os
from dotenv import load_dotenv
from . import auth

# Load environment variables
load_dotenv()

app = FastAPI(title="Remote Wake-on-LAN")

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if not auth.verify_credentials(username, password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    return auth.create_login_response(username)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    user = auth.get_current_user(request)
    if not user:
        return """
        <!DOCTYPE html>
        <html>
            <head>
                <title>Remote Wake-on-LAN - Login</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        max-width: 400px;
                        margin: 0 auto;
                        padding: 20px;
                        text-align: center;
                    }
                    form {
                        background: #f9f9f9;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }
                    input {
                        width: 100%;
                        padding: 8px;
                        margin: 10px 0;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                        box-sizing: border-box;
                    }
                    button {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 10px 20px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 10px 0;
                        cursor: pointer;
                        border-radius: 4px;
                        width: 100%;
                    }
                    button:hover {
                        background-color: #45a049;
                    }
                </style>
            </head>
            <body>
                <h1>Remote Wake-on-LAN</h1>
                <form action="/login" method="post">
                    <input type="text" name="username" placeholder="Username" required>
                    <input type="password" name="password" placeholder="Password" required>
                    <button type="submit">Login</button>
                </form>
            </body>
        </html>
        """

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
                .logout {
                    position: absolute;
                    top: 20px;
                    right: 20px;
                    background-color: #f44336;
                }
                .logout:hover {
                    background-color: #da190b;
                }
            </style>
        </head>
        <body>
            <h1>Remote Wake-on-LAN</h1>
            <button class="logout" onclick="logout()">Logout</button>
            <button onclick="wakeComputer()">Wake Computer</button>
            <div id="status"></div>
            <script>
                async function wakeComputer() {
                    const statusDiv = document.getElementById('status');
                    try {
                        const response = await fetch('/wake', {
                            method: 'POST',
                            credentials: 'include'
                        });
                        const data = await response.json();
                        statusDiv.textContent = data.message;
                        statusDiv.className = response.ok ? 'success' : 'error';
                    } catch (error) {
                        statusDiv.textContent = 'Error: ' + error.message;
                        statusDiv.className = 'error';
                    }
                }

                async function logout() {
                    try {
                        await fetch('/logout', {
                            method: 'POST',
                            credentials: 'include'
                        });
                        window.location.href = '/';
                    } catch (error) {
                        console.error('Logout failed:', error);
                    }
                }
            </script>
        </body>
    </html>
    """

@app.post("/wake")
async def wake_computer(request: Request):
    auth.require_auth(request)

    TARGET_MAC = os.getenv("TARGET_MAC")
    if not TARGET_MAC:
        raise HTTPException(status_code=500, detail="Target MAC address not configured")

    try:
        send_magic_packet(TARGET_MAC)
        return {"message": "Wake-on-LAN packet sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send wake packet: {str(e)}")

@app.post("/logout")
async def logout():
    return auth.create_logout_response()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
