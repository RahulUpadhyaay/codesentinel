from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from app.database import get_session
from app.models.user import User
from app.core.security import decode_access_token

# Simple HTTP Bearer Security Scheme (Swagger UI will show a clean JWT input box!)
security_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    session: Session = Depends(get_session)
) -> User:
    """
    Dependency that protects endpoints. Extracts and verifies JWT token from Authorization header.
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 1. Decode token
    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception
        
    user_id: str = payload.get("sub")
    if not user_id:
        raise credentials_exception
        
    # 2. Fetch user from database
    user = session.get(User, int(user_id))
    if not user:
        raise credentials_exception
        
    return user