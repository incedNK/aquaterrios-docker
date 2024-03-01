from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from crud import users
from db.database import get_db
from schema.users import Login
from utils.auth import security, verify_token, verify_password



def get_current_user(db: Session = Depends(get_db), token: str=Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token, credentials_exception)  
    current_user = users.get_user(db, username=token_data.username)
    if current_user is None:
        raise credentials_exception
    
    return current_user


def validate_user(db: Session, user: Login):
    db_user = users.get_user(db=db, username=user.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )   

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return db_user

