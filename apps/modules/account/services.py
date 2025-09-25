from apps.mongo.base import BaseCRUD
from apps.mongo.engine import engine_makeup
from apps.auth.services import auth_services
from .schemas import LoginRequest, ForgotPasswordRequest
from apps.modules.emails.controllers import EmailController
from apps.utils.helper import Helper
from .exception import ErrorCode


account_crud = BaseCRUD("users", engine_makeup)


class AccountService:
    def __init__(self, crud: BaseCRUD):
        self.crud = crud
        self.email_controller = EmailController()

    async def login(self, data: LoginRequest):
        email = data.email
        user = await self.crud.get_one_query({"email": email})
        if not user:
            raise ErrorCode.InvalidLogin()

        if not auth_services.check_password(data.password, user["password"].encode()):
            raise ErrorCode.InvalidLogin()

        token_data = {
            "uid": str(user.get("_id")),
            "email": user.get("email"),
            "permission": user.get("permission"),
            "remember_me": data.remember_me
        }
        token = await auth_services.encode_access_token(token_data)

        return {"token_type": "bearer", "access_token": token}

    async def get_otp(self, email: str):
        user = await self.crud.get_one_query({"email": email})
        if not user: 
            raise ErrorCode.EmailNotFound()

        otp_code = Helper.generate_secret_otp()
        otp_exp = Helper.get_timestamp() + 5 * 60

        await self.crud.update_by_id(_id=user["_id"], data={"otp_code": otp_code, "otp_exp": otp_exp})

        await self.email_controller.send_producer(
            email=user["email"], fullname=user["fullname"],
            data={"otp_code": otp_code}, mail_type="reset_password"
        )

        return {"message": f"OTP sent to {email} and valid for 5 minutes"}
    
    
    async def forgot_password(self, data: ForgotPasswordRequest):
        user = await self.crud.get_one_query({"email": data.email})
        if not user:
            raise ErrorCode.EmailNotFound()
        
        if "otp_code" not in user or "otp_exp" not in user:
            raise ErrorCode.OTPNotFound()
        
        if user["otp_code"] != data.otp_code:
            raise ErrorCode.InvalidOTP()
        
        if Helper.get_timestamp() > user["otp_exp"]:
            raise ErrorCode.ExpiredOTP()
        
        hashed_password = (await auth_services.hash_password(data.new_password)).decode()

        await self.crud.update_no_limit(
            {"_id": user["_id"]},
            {
                "$set": {"password": hashed_password},
                "$unset": {"otp_code": "", "otp_exp": ""}
            }
        )
        return {"message": "Password has been reset successfully"}
