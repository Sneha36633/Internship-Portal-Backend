from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

# Import all the necessary modules from your application structure
from ..schemas import user_schemas
from ..models import user_model
from ..crud import user_crud
from .. import auth
from ..config.database import get_db

# Create a new router instance
router = APIRouter()

@router.post("/register", response_model=user_schemas.User)
def register_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    Checks if a user with the same email already exists.
    """
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create the new user in the database
    return user_crud.create_user(db=db, user=user)


@router.post("/login")
def login_for_access_token(form_data: user_schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Log in a user.
    Verifies email and password, then returns a JWT token.
    """
    user = user_crud.get_user_by_email(db, email=form_data.email)
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create the JWT token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

