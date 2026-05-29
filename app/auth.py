from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the necessary modules from your application structure
from .schemas import user_schemas
from .crud import user_crud
from .config.database import get_db

# --- Password Hashing Setup ---
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- JWT Configuration ---
SECRET_KEY = os.getenv("SECRET_KEY", "your_super_secret_key_that_is_long_and_random_fallback_for_dev")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# This creates an instance of OAuth2PasswordBearer.
# The `tokenUrl` points to the endpoint that the client will use to get the token (your login route).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# --- Utility Functions ---

def verify_password(plain_password, hashed_password):
    """Verifies a plain password against a hashed one."""
    # Bcrypt has a 72-byte limit, truncate if necessary
    if len(plain_password) > 72:
        plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Hashes a plain password."""
    # Bcrypt has a 72-byte limit, truncate if necessary
    if len(password) > 72:
        password = password[:72]
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Creates a new JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default expiration time if none is provided
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# --- Dependency for Protected Routes ---

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    This function is a dependency that can be injected into any path operation.
    It takes the token from the request's Authorization header, verifies it,
    and returns the corresponding user from the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT to get the payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # The "sub" (subject) of our token is the user's email
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        # This will catch any errors during decoding (e.g., expired token)
        raise credentials_exception
    
    # Get the user from the database using the email from the token
    user = user_crud.get_user_by_email(db, email=email)
    if user is None:
        # If the user doesn't exist (e.g., they were deleted), the token is invalid
        raise credentials_exception
    
    return user

