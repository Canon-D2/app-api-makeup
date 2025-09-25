from bson import ObjectId
from zoneinfo import ZoneInfo
from typing import Optional
from apps.utils.validator import Validator
import time, datetime, string, secrets

class Helper:
    
    @staticmethod
    def get_timestamp() -> float:
        timestamp = time.time()
        return timestamp

    @staticmethod
    def object_to_string(doc: dict) -> dict:
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc
    
    @staticmethod
    def string_to_object(query: dict) -> dict:
        if "_id" in query and isinstance(query["_id"], str) and Validator.is_object_id(query["_id"]):
            query["_id"] = ObjectId(query["_id"])
        return query
    
    @staticmethod
    def get_future_timestamp(days_to_add: int) -> float:
        current_date = datetime.datetime.now()
        future_date = current_date + datetime.timedelta(days=days_to_add)
        return future_date.timestamp() 

    @staticmethod
    def timestamp_to_date(ts: float, fmt: str = "%d-%m-%Y %H:%M:%S", tz: Optional[str] = "Asia/Ho_Chi_Minh") -> str:
        # Convert timestamp (e.g., 1755688756) to date string "20-08-2025 22:59:16"
        # Timezone ex: Asia/Tokyo, None, UTC,...
        result = datetime.datetime.fromtimestamp(float(ts), tz=ZoneInfo(tz))
        return result.strftime(fmt)

    @staticmethod
    def date_to_timestamp(date_str: str, fmt: str = "%d-%m-%Y %H:%M:%S", tz: Optional[str] = "Asia/Ho_Chi_Minh") -> float:
        # Convert date string "20-08-2025 22:59:16" to timestamp (e.g., 1755688756.0)
        result = datetime.datetime.strptime(date_str, fmt)
        result = result.replace(tzinfo=ZoneInfo(tz))
        return result.timestamp()
    
    @staticmethod
    def generate_secret_otp(length: int = 6) -> str:
        chars = string.ascii_uppercase + string.digits
        while True:
            otp_code = ''.join(secrets.choice(chars) for _ in range(length))
            if sum(c.isalpha() for c in otp_code) >= 2 and sum(c.isdigit() for c in otp_code) >= 2:
                return otp_code