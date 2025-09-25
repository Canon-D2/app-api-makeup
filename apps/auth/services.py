from jose import jwt
from apps.mongo.base import BaseCRUD
from apps.utils.helper import Helper
from apps.mongo.engine import engine_makeup
from bcrypt import checkpw, gensalt, hashpw

from .config import ACCESS_TOKEN_EXPIRE_DAY, ALGORITHM, REMEMBER_TOKEN_DAY, SECRET_KEY


class AuthServices():
    def __init__(self, crud, service_name: str, owner_type: str = None):
        self.crud = crud
        self.service_name = service_name
        self.owner_type = owner_type

    async def hash_password(self, password):
        result = hashpw(password.encode("utf8"), gensalt())
        return result

    def check_password(self, user_login_password, password):
        if not checkpw(user_login_password.encode("utf-8"), password):
            return False
        return True

    async def encode_access_token(self, data):
        data = data.copy()
        expire_days = (REMEMBER_TOKEN_DAY if data.get("remember_me") else ACCESS_TOKEN_EXPIRE_DAY)
        
        expire = Helper.get_future_timestamp(days_to_add=expire_days)
        
        data.update({"exp": expire})
        
        encode = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return encode


auth_crud = BaseCRUD("auth", engine_makeup)
auth_services = AuthServices(crud=auth_crud, service_name="auth services")
