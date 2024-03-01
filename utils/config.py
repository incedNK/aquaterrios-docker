from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_user: str 
    postgres_password: str 
    postgres_server: str 
    postgres_port: str 
    postgres_db_name: str 
    
    secret_key :str   
    algorithm: str                        
    access_token_expire_minutes: int
    
    email : str 
    password: str
    
    
    class Config:
        env_file = ".env"
    

settings = Settings()