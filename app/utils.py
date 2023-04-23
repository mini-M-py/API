from passlib.context import CryptContext
import string
import random
import time
from cachetools import TTLCache
from fastapi import status, HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")


cache = TTLCache(maxsize=100, ttl=60)
def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def generate_otp(length=6):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def save_otp(email, otp):
    cache[email] = otp

def verify_otp(email: str, otp: str) -> bool:
    cached_otp = cache.get(email)

    if cached_otp is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP not found or expired")
    if cached_otp != otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")

    del cache[email]
    return True




