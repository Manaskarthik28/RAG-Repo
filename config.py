from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()

class Settings(BaseModel):
    user_name: str = os.getenv("USER_NAME", "")
    password: str = os.getenv("PASSWORD", "")
    jwt_secret: str = os.getenv("JWT_SECRET", "")
    algo:str = os.getenv("ALGO", "")

settings = Settings()

