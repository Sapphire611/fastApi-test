import hashlib
import re
from app.core.config import settings


def hash_password_sha256(password: str) -> str:
    """SHA-256(password + PASSWORD_SALT) → hex string, matching INFP-CMS frontend"""
    salted = password + settings.PASSWORD_SALT
    return hashlib.sha256(salted.encode("utf-8")).hexdigest()


def is_sha256_hex(s: str) -> bool:
    """Check if a string looks like a SHA-256 hex digest (64 hex chars)"""
    return bool(re.fullmatch(r"[a-f0-9]{64}", s, re.IGNORECASE))
