from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import os

# -----------------------------
# 🔐 Configuration
# -----------------------------

# You can set this in your .env file for security:
# SECRET_KEY=your_super_secret_key
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_fallback")  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# -----------------------------
# 🔑 Password Hashing
# -----------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hashed version."""
    # bcrypt supports only first 72 bytes
    if len(plain_password.encode()) > 72:
        plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)


# -----------------------------
# 🧾 JWT Token Creation
# -----------------------------
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
