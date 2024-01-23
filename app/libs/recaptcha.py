import json

import requests
from fastapi import HTTPException, status

from app.config import RE_CAPTCHA_SECRET


def verify_captcha(captcha_token: str):
    url = "https://www.google.com/recaptcha/api/siteverify"
    multipart_form_data = {
        "secret": (None, RE_CAPTCHA_SECRET),
        "response": (None, captcha_token),
    }
    response = requests.post(url, files=multipart_form_data)
    if response.status_code == 200:
        data = json.loads(response.text)
        if data["success"] == False:
            print(data)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Captcha verification failed.",
            )
    else:
        print(response.status_code, response.text)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create user.",
        )
