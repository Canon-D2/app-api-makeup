from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:

    @staticmethod
    def InvalidInvoiceId():
        return StandardException(
            type="invoices/error/invalid-id",
            status=status.HTTP_400_BAD_REQUEST,
            title="Invalid invoice id",
            detail="The invoice id provided is not valid"
        )
    
    @staticmethod
    def ArtistNotSchedule():
        return StandardException(
            type="invoices/error/not-schedule",
            status=status.HTTP_400_BAD_REQUEST,
            title="Artist Not Schedule",
            detail="Artist chưa có lịch làm việc trong ngày này"
        )
    
    @staticmethod
    def ArtistNotFree():
        return StandardException(
            type="invoices/error/not-free-booking",
            status=status.HTTP_400_BAD_REQUEST,
            title="Artist Not Free Booking",
            detail="Khoảng thời gian không nằm trong khung giờ rảnh của artist"
        )
    
    @staticmethod
    def DuplicateBooking():
        return StandardException(
            type="invoices/error/exist-invoice",
            status=status.HTTP_400_BAD_REQUEST,
            title="Artist Duplicate Invoice",
            detail="Artist đã có lịch trong khung giờ với khách khác"
        )