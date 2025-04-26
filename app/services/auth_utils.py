import jwt
import os
from datetime import datetime, timedelta
from fastapi import HTTPException, Cookie, Depends, Header
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = "CHANGE_ME_SECRET"
ALGORITHM = "HS256"
ACCESS_EXPIRES_MIN = 60 * 24

# Load admin account từ .env
admin_usernames = os.getenv('ADMIN_USERS', '').split(',')
admin_passwords = os.getenv('ADMIN_PASSWORDS', '').split(',')
ADMIN_USERS = dict(zip(admin_usernames, admin_passwords))


def create_access_token(payload: dict, minutes: int = ACCESS_EXPIRES_MIN):
    to_encode = payload.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=minutes)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Hết phiên đăng nhập.")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token không hợp lệ.")


def verify_user(conn, username: str, plain_pw: str):
    # Nếu là admin
    if username in ADMIN_USERS and ADMIN_USERS[username] == plain_pw:
        return {"username": username, "role": "admin"}

    # Nếu không phải admin --> kiểm tra DB
    from psycopg2.extras import RealDictCursor
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT check_password(%s, %s)", (username, plain_pw))
        result = cur.fetchone()
        if not result or not result["check_password"]:
            return None
        return {"username": username, "role": "user"}  # role user mặc định


def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Thiếu hoặc sai định dạng Authorization")

    token = authorization.split("Bearer ")[1]
    payload = decode_access_token(token)
    username = payload.get("sub")
    role = payload.get("role", "user")  # mặc định role=user nếu không có

    if not username:
        raise HTTPException(status_code=401, detail="Token không hợp lệ.")

    return {"username": username, "role": role}
