from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, TokenResponse, UserResponse
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# ==========================================
# 1. REGISTER NEW USER
# ==========================================
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister, session: Session = Depends(get_session)):
    # A. Check if email already exists in DB
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )
    
    # B. Hash the plain text password
    secure_hash = hash_password(user_data.password)
    
    # C. Save user to Database
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=secure_hash
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return new_user


# ==========================================
# 2. LOGIN USER & RETURN JWT TOKEN
# ==========================================
@router.post("/login", response_model=TokenResponse)
def login_user(credentials: UserLogin, session: Session = Depends(get_session)):
    # A. Find user by email
    user = session.exec(select(User).where(User.email == credentials.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
        
    # B. Verify input password against stored hash
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
        
    # C. Generate JWT Access Token
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_name=user.full_name
    )