from sqlalchemy.orm import Session

from db import models
from schema.users import UserCreate, SubscriberCreate, NoteCreate, UserUpdate, AdminUserUpdate, UpdateNote, LostPassword, ResetPassword
from utils.auth import get_hashed_password, generate_secret

# Handling users
def get_user(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    return user

def get_user_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user

def get_user_by_secret(db: Session, secret: str):
    user = db.query(models.User).filter(models.User.secret == secret).first()
    return user

def get_users(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    db_user = models.User(email=user.email, username = user.username, hashed_password=get_hashed_password(user.password), 
        name=user.name, surname=user.surname, address=user.address, admin=user.admin, premium=user.premium, delisted=user.delisted, 
        secret=generate_secret())
    if db_user.username == "admin":
        db_user.delisted = False
        db_user.admin = True
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def change_password(db: Session, username: str, password: LostPassword):
    pwd_query = db.query(models.User).filter(models.User.username == username)
    if not pwd_query.first():
        return False
    hashed_pwd = get_hashed_password(password.password)
    pwd_query.update({models.User.hashed_password: hashed_pwd}, synchronize_session=False)
    db.commit()
    return True

def reset_password(db: Session, password: ResetPassword):
    reset_query = db.query(models.User).filter(models.User.secret == password.secret)
    if not reset_query.first():
        return False
    hashed_pwd = get_hashed_password(password.password)
    reset_query.update(
        {
            models.User.hashed_password: hashed_pwd,
            models.User.secret: generate_secret()
        }, 
        synchronize_session=False)
    db.commit()
    return True

def update_user(db: Session, username: str, user: UserUpdate):
    user_query = db.query(models.User).filter(models.User.username == username)
    if not user_query.first():
        return False
    user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    return True

def admin_update_user(db: Session, username: str, user: AdminUserUpdate):
    user_query = db.query(models.User).filter(models.User.username == username)
    if not user_query.first():
        return False
    user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    return True

def delete_user(username: str , db: Session):
    existing_user = db.query(models.User).filter(models.User.username == username)
    if not existing_user.first():
        return False
    existing_user.delete(synchronize_session=False)
    db.commit()
    return True

# Handle new subscribers
def get_subscribers(db: Session):
    return db.query(models.Subscription).all()

def get_subscriber(db: Session, mail: str):
    return db.query(models.Subscription).filter(models.Subscription.mail == mail).first()

def get_subscriber_by_id(db: Session, id: int):
    return db.query(models.Subscription).filter(models.Subscription.id == id).first()

def subscribe(db: Session, new_subscriber: SubscriberCreate):
    subscriber = models.Subscription(mail=new_subscriber.mail)
    db.add(subscriber)
    db.commit()
    db.refresh(subscriber)
    return subscriber

def delete_subscriber(subscriber_id: int, db: Session):
    existing_subscriber = db.query(models.Subscription).filter(models.Subscription.id == subscriber_id)
    if not existing_subscriber.first():
        return False
    existing_subscriber.delete(synchronize_session=False)
    db.commit()
    return True

# In system messages to users by admin
def alerts(db: Session):
    return db.query(models.Notification).all()

def user_alerts(db: Session, user: str):
    alerts = db.query(models.Notification).filter(models.Notification.user == user).all()
    return alerts

def user_alert(db: Session, note_id: int):
    alert = db.query(models.Notification).filter(models.Notification.id == note_id).first()
    return alert

def create_alert(db: Session, new_alert: NoteCreate):
    notification = models.Notification(user=new_alert.user, message=new_alert.message, read=new_alert.read)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def update_alert(db: Session, note: UpdateNote, note_id: int):
    note_query = db.query(models.Notification).filter(models.Notification.id == note_id)
    if not note_query.first():
        return False
    note_query.update(note.dict(), synchronize_session=False)
    db.commit()
    return True

def delete_alert(note_id: int, db: Session):
    existing_note = db.query(models.Notification).filter(models.Notification.id == note_id)
    if not existing_note.first():
        return False
    existing_note.delete(synchronize_session=False)
    db.commit()
    return True

def delete_viewed_alerts(db: Session, user: str):
    viewed_notes = db.query(models.Notification).filter(models.Notification.read == True and models.Notification.user == user)
    if not viewed_notes.all():
        return False
    viewed_notes.delete(synchronize_session=False)
    db.commit()
    return True