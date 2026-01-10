import secrets
import uuid
import jwt
from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import HTTPException, status

from config import settings


def generate_uuid() -> str:
    return uuid.uuid4().hex


def generate_secret_code() -> str:
    digits = "0123456789"
    return "".join(
        secrets.choice(digits) for _ in range(settings.verification.code_len)
    )


def encode_jwt(
    payload: dict,
    private_key: str = settings.jwt.private.read_text(),
    algorithm: str = settings.jwt.algoritm,
    expire_minutes: int = settings.jwt.ttl * 60,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=expire,
        iat=now,
    )

    encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)

    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.jwt.public.read_text(),
    algorithm: str = settings.jwt.algoritm,
) -> dict:

    try:
        decoded = jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=[algorithm],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )

    return decoded


def hash_password(
    password: str,
) -> str:
    salt = bcrypt.gensalt()
    pw_bytes = password.encode()
    return bcrypt.hashpw(pw_bytes, salt).decode("utf-8")


def verify_password(
    password: str,
    hashed_password: str,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(), hashed_password=hashed_password.encode()
    )
