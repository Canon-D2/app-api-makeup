from datetime import datetime
from zoneinfo import ZoneInfo
from .exception import ErrorCode
from apps.mongo.base import BaseCRUD
from apps.mongo.engine import engine_makeup

invoice_crud = BaseCRUD("invoices", engine_makeup)
booking_crud = BaseCRUD("bookings", engine_makeup) 

VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")

class InvoiceServices:
    def __init__(self, crud: BaseCRUD):
        self.crud = crud
        self.invoice_crud = self.crud
        self.booking_crud = booking_crud

    async def create(self, data: dict):
        # S1: Check if the artist has set a schedule for that day
        booking_date = datetime.fromtimestamp(data["start_time"], VN_TZ).strftime("%Y-%m-%d")
        booking_schedule = await self.booking_crud.get_one_query({"artist_id": data["artist_id"],"date": booking_date})

        if not booking_schedule: raise ErrorCode.ArtistNotSchedule()

        # S2: Check duration in collection Booking
        freetime = False
        for slot in booking_schedule.get("freetime", []):
            if data["start_time"] >= slot["start_free"] and data["end_time"] <= slot["end_free"]:
                freetime = True
                break

        if not freetime: raise ErrorCode.ArtistNotFree()

        # S3: Check duration in collection Invoice
        conflict_invoice = await self.invoice_crud.get_one_query({
            "artist_id": data["artist_id"],
            "status": {"$in": ["pending", "confirmed"]},
            "$and": [
                {"start_time": {"$lt": data["end_time"]}, "end_time": {"$gt": data["start_time"]}} 
            ]
        })

        if conflict_invoice: raise ErrorCode.DuplicateBooking()

        result = await self.invoice_crud.create(data)
        return result

    async def update(self, _id, data: dict):
        result = await self.invoice_crud.update_by_id(_id, data)
        if not result:
            raise ErrorCode.InvalidInvoiceId()
        return result

    async def get(self, _id):
        result = await self.invoice_crud.get_by_id(_id)
        if not result:
            raise ErrorCode.InvalidInvoiceId()
        return result

    async def delete(self, _id):
        result = await self.invoice_crud.delete_by_id(_id)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.invoice_crud.search(query, page, limit)
        return result
