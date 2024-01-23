import json
import os

from fastapi import HTTPException, status

# DB_HOST = os.environ.get("PRO_DB_HOST")
# DB_USER = os.environ.get("PRO_DB_USER")
# DB_PASSWORD = os.environ.get("PRO_DB_PASSWORD")
# DB_NAME = os.environ.get("PRO_DB_NAME")
# JWT_KEY = os.environ.get("PRO_JWT_KEY")
# RE_CAPTCHA_SECRET = os.environ.get("PRO_RE_CAPTCHA_SECRET")
# SES_FROM_EMAIL = os.environ.get("PRO_SES_FROM_EMAIL")
# BUCKET_NAME = os.environ.get("PRO_BUCKET_NAME")

DB_HOST = "localhost"
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_NAME = "projectx"
JWT_KEY = '{"k":"xuQvsl68aTATKRhHjBYo1msJckIJqAj9PooXELeojpY","kty":"oct"}'
RE_CAPTCHA_SECRET = os.environ.get("PRO_RE_CAPTCHA_SECRET")
SES_FROM_EMAIL = os.environ.get("PRO_SES_FROM_EMAIL")
BUCKET_NAME = os.environ.get("PRO_BUCKET_NAME")

if JWT_KEY:
    try:
        JWT_KEY = json.loads(JWT_KEY)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT key"
        )
else:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="JWT key not set"
    )
