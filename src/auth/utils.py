# src/auth/utils.py
from passlib.context import CryptContext
from datetime import timedelta, datetime
from src.config import Config
import jwt
from uuid import uuid4
import logging
from itsdangerous import URLSafeTimedSerializer

passwd_context = CryptContext(schemes=['bcrypt'])

ACCESS_TOKEN_EXPIRY = 3600

def generate_password_hash(password: str) -> str:
    hash = passwd_context.hash(password)
    return hash

def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {}

    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid4())
    payload['refresh'] = refresh

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )
    #print(f"'token': {token}")  # print statement
    return token

def decode_token(token: str) -> dict:
    #print(f"'token' decode_token: {token}")
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM]
        )
        #print(f"'token_data': {token_data}")  # print statement
        return token_data
    except jwt.PyJWKError as e:
        logging.exception(e)
        return None

serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET_KEY, salt="email-configuration"
)

def create_url_safe_token(data: dict):
    """
    Serialize a dict into a URLSafe token 
    'Python Dictionary (JSON Object)' --> 'JSON String'
    """
    token = serializer.dumps(data)

    return token

def decode_url_safe_token(token:str):
    """
    Deserialize a URLSafe token to get data
    'JSON String' --> 'Python Dictionary (JSON Object)'
    """
    try:
        token_data = serializer.loads(token)

        return token_data
    
    except Exception as e:
        logging.error(str(e))

  