from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.config import settings

# 1. Setup Password Hashing Context using Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==========================================
# A. PASSWORD HASHING & VERIFICATION
# ==========================================

def hash_password(password: str) -> str:
    """Takes a plain text password and returns a secure bcrypt hash."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if a user's input password matches the stored bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ==========================================
# B. JWT TOKEN CREATION & DECODING
# ==========================================

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Generates a signed JWT Access Token containing payload data (like user ID or email).
    """
    to_encode = data.copy()
    
    # Calculate token expiration timestamp
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    
    # Sign token using secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodes and verifies a JWT token. Returns payload dict or None if invalid/expired.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None