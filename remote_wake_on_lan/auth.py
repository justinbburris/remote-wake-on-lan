from fastapi import HTTPException, Request, Response, Form
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import os
import secrets
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
AUTH_USERNAME = os.getenv("AUTH_USERNAME")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
IS_PRODUCTION = os.getenv("ENVIRONMENT", "development") == "production"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify a JWT token and return its payload if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_current_user(request: Request) -> Optional[dict]:
    """Get the current user from the session cookie."""
    token = request.cookies.get("session")
    if not token:
        return None
    return verify_token(token)

def verify_credentials(username: str, password: str) -> bool:
    """Verify username and password against configured credentials."""
    correct_username = secrets.compare_digest(username, AUTH_USERNAME)
    correct_password = secrets.compare_digest(password, AUTH_PASSWORD)
    return correct_username and correct_password

def create_login_response(username: str) -> Response:
    """Create a response with a new session cookie."""
    access_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(
        key="session",
        value=access_token,
        httponly=True,
        secure=IS_PRODUCTION,  # Only require HTTPS in production
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return response

def create_logout_response() -> Response:
    """Create a response that clears the session cookie."""
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("session")
    return response

def require_auth(request: Request) -> None:
    """Raise an HTTPException if the user is not authenticated."""
    if not get_current_user(request):
        raise HTTPException(status_code=401, detail="Not authenticated")
