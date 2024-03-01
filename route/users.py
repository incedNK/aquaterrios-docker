from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from schema.users import User, UserCreate, Token, SubscriberCreate, ResetPassword
from utils.auth import create_access_token
from utils import auth
from db.database import get_db
from crud import users, login

user_router = APIRouter()


@user_router.post("/register")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = users.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Username already exists")
    user_mail= users.get_user_email(db, email=user.email)
    if user_mail:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Email already exists")
    user = users.create_user(user=user, db=db)
    return {"detail": "New user was created successfully"}

@user_router.patch("/reset_password/{secret}")
def user_reset_password(password: ResetPassword, db: Session = Depends(get_db)):
    password_to_update = users.get_user_by_secret(db=db, secret=password.secret)
    if not password_to_update:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Could not found user in database"
        )
    try:
        users.reset_password(db=db, password=password)
        return {"detail": "Successfully changed password"}
    except:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = "Something went wrong with connection to database"
        )

@user_router.get("/get_key/{username}")
def get_secret_key(username: str, db: Session = Depends(get_db)):
    user = users.get_user(db=db, username=username)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="Couldn't find user",
        )
    else:
        auth.send_key_to_mail(email=user.email, key=user.secret)
        return RedirectResponse("/reset", status_code=status.HTTP_302_FOUND)
        

@user_router.post("/login", response_model=Token)
def log_user(user: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    db_user = login.validate_user(db=db, user=user)

    if not db_user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(
        data={"sub": user.username}
    )
    # return {"access_token": access_token, "token_type": "bearer"}
    
    token = jsonable_encoder(access_token)
    content = {"detail": "You've successfully logged in. Wellcome back!"}
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="Lax",
        secure=False,
    )
    return response

@user_router.post("/subscribe")
def subscribe(subscriber: SubscriberCreate, db: Session = Depends(get_db)):
    applicant = users.get_subscriber(db=db, mail=subscriber.mail)
    if applicant:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Email already exists")
    users.subscribe(db=db, new_subscriber=subscriber)
    return {"detail": "Thank you for your registration."}

@user_router.get("/users", response_model=List[User])
def read_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    db_users = users.get_users(db=db, skip=skip, limit=limit)
    return db_users