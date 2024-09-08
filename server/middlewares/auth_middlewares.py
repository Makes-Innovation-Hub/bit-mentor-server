from fastapi import Request
import jwt
from setting.config import config

# check if a user is logged in
def check_token(request: Request):
        auth_header = request.headers.get('authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                if verify_jwt(token):
                    return request
            except Exception as e:
                raise e
        return

def verify_jwt(token: str):
    try:
        data = jwt.decode(token, config.JWT_KEY, algorithms="HS256")
        return data["telegram_user"]
    except Exception as e:
        print('e: ', e)
        print("bad token")
        return False