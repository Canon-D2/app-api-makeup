import re
from bson import ObjectId

class Validator:

    @staticmethod
    def is_object_id(_id: str) -> bool:
        result =  ObjectId.is_valid(_id)
        return result
    
    @staticmethod
    async def is_email_exists(crud, email: str, exclude_id: str = None) -> bool:
        if not email: 
            return False
        query = {"email": email}
        if exclude_id:
            query["_id"] = {"$ne": ObjectId(exclude_id)}
        existing = await crud.get_one_query(query=query)
        return existing is not None

    @staticmethod
    def is_password_valid(password: str) -> bool:
        if not 8 <= len(password) <= 12:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[0-9]", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True
    
    @staticmethod
    def is_vietnamese_phone(phone: str) -> bool:
        # Start with valid mobile numbers (3,5,7,8,9)
        pattern = r"^(?:\+84|0)(3|5|7|8|9)\d{8}$"
        return re.match(pattern, phone) is not None
