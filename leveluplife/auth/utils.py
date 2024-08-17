from passlib.context import CryptContext
from leveluplife.settings import Settings

settings = Settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
