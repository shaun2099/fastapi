import os

from pydantic import BaseSettings

path = os.getenv("Path")
print(path)



class Settings(BaseSettings):
    db_pwd: str 
    db_user: str 
    secret_key: str

    class Config:
        env_file = 'app\\.env'
        env_file_encoding = 'utf-8'

settings = Settings()