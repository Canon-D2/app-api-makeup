from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:

    @staticmethod
    def InvalidBooking():
        return StandardException(
            type="booking/error/invalid-id",
            status=status.HTTP_404_NOT_FOUND,
            title="Booking service not found",
            detail="The booking ID provided does not exist."
        )
    
    @staticmethod
    def DateExist():
        return StandardException(
            type="booking/error/date-exist",
            status=status.HTTP_404_NOT_FOUND,
            title="Date of artist have exist",
            detail="This artist's blank space already exists, please check again."
        )