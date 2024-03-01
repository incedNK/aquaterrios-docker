from typing import Optional, Union
from datetime import datetime, timedelta
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from jose import JWTError, jwt
from passlib.context import CryptContext

from utils.config import settings
from schema.users import TokenData


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        token_url: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": token_url, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=401,
                    detail="You are not loged in. Go to Home page and login again.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None

        return param


security = OAuth2PasswordBearerCookie(token_url="/login")


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_hashed_password(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
  
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
    
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    return token_data
    
def generate_secret():
    return ''.join(random.choices('0123456789abcdefghijklmnopqrsty', k=16))

def send_key_to_mail(email: str, key: str):
    port = 587
    smtp_server = "smtp-mail.outlook.com"
    sender = settings.email
    receiver = email
    password = settings.password
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Request for secret key"
    msg["From"] = sender
    msg["To"] = receiver
    
    text = f"Hello.\nYour secret key:\n {key}\nWith regards.\nAgritech Team"
    body = MIMEText(text, 'plain')
    msg.attach(body)
    
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    print("Email was sent!")
    server.quit()
