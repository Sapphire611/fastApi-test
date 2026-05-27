"""Migrate a user password from old format (bcrypt(plain)) to new format (bcrypt(SHA-256(plain+salt)))"""
import asyncio
import hashlib
import sys
import bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Must match frontend's NEXT_PUBLIC_PASSWORD_SALT
SALT = "infp-cms-fixed-salt-2024"


def hash_new_format(plain: str) -> str:
    sha256 = hashlib.sha256((plain + SALT).encode()).hexdigest()
    return pwd_context.hash(sha256)


async def migrate_user(supabase_url: str, supabase_key: str, username: str, plain: str):
    from supabase import create_client

    client = create_client(supabase_url, supabase_key)

    # Look up user
    result = client.table("users").select("*").eq("username", username).execute()
    if not result.data:
        print(f"User not found: {username}")
        return

    user = result.data[0]
    stored = user["password"]

    # Check current format
    is_bcrypt = stored.startswith("$2b$") or stored.startswith("$2a$")

    if is_bcrypt and bcrypt.checkpw(plain.encode(), stored.encode()):
        print(f"Current format: bcrypt(plain) — old format, needs migration")
    else:
        sha256_hex = hashlib.sha256((plain + SALT).encode()).hexdigest()
        if is_bcrypt and bcrypt.checkpw(sha256_hex.encode(), stored.encode()):
            print(f"Current format: bcrypt(SHA256(pwd+salt)) — already new format, no migration needed")
            return
        else:
            print(f"Cannot verify password format. Stored: {stored[:30]}...")
            return

    # Migrate
    new_hash = hash_new_format(plain)
    client.table("users").update({"password": new_hash}).eq("id", user["id"]).execute()
    print(f"Migrated user: {username} (id={user['id']})")
    print(f"Old: {stored[:30]}...")
    print(f"New: {new_hash[:30]}...")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python scripts/migrate_password.py <supabase_url> <supabase_key> <username> <plain_password>")
        print("  Migrates a user from bcrypt(plain) to bcrypt(SHA256(plain+salt))")
        sys.exit(1)

    asyncio.run(migrate_user(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
