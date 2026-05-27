"""Diagnostic: test which password format matches a stored bcrypt hash"""
import hashlib
import sys
import bcrypt

stored = "$2b$10$2QdGnRmyOgo.WiZAF95.COTcVsHEdPRkWNu5flAFVjpqd/jVgIyeC"

# Salt must match frontend's NEXT_PUBLIC_PASSWORD_SALT
SALT = "infp-cms-fixed-salt-2024"

if len(sys.argv) < 2:
    print("Usage: python scripts/check_password.py <plain_password> [salt]")
    print("  Tests which hashing format matches the stored bcrypt hash")
    sys.exit(1)

plain = sys.argv[1]
salt = sys.argv[2] if len(sys.argv) > 2 else SALT

print(f"Testing with salt: {salt}")
print(f"Stored bcrypt:  {stored[:30]}...")
print()

# Test 1: bcrypt(plain password) — old format
match1 = bcrypt.checkpw(plain.encode(), stored.encode())
print(f"Test 1: bcrypt(plain)              → {'MATCH' if match1 else 'no match'}")

# Test 2: bcrypt(SHA-256(plain + salt)) — new format (INFP-CMS)
sha256 = hashlib.sha256((plain + salt).encode()).hexdigest()
match2 = bcrypt.checkpw(sha256.encode(), stored.encode())
print(f"Test 2: bcrypt(SHA256(pwd+salt))   → {'MATCH' if match2 else 'no match'}")

# If neither matches, try different salts
if not match1 and not match2:
    print()
    print("Neither matched. Try with a different --salt value.")
    print(f"SHA-256 hex that was tested: {sha256}")
