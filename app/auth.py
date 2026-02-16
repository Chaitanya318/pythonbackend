import bcrypt
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


# ==========================
# HASH PASSWORD
# ==========================
def hash_password(password: str):

    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed.decode("utf-8")


# ==========================
# VERIFY PASSWORD
# ==========================
def verify_password(password: str, hashed: str):

    password_bytes = password.encode("utf-8")

    hashed_bytes = hashed.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hashed_bytes)


# ==========================
# CREATE JWT TOKEN
# ==========================
def create_token(data: dict):

    expire = datetime.utcnow() + timedelta(days=1)

    data.update({"exp": expire})

    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return token
