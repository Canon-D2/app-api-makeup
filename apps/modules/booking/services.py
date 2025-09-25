from apps.mongo.base import BaseCRUD
from apps.mongo.engine import engine_makeup
from .exception import ErrorCode


booking_crud = BaseCRUD("bookings", engine_makeup)

class BookingServices:
    def __init__(self, crud: BaseCRUD):
        self.crud = crud
    
    async def create(self, data: dict):
        exist = await self.crud.get_one_query({"artist_id": data["artist_id"], "date": data["date"]})
        if exist:
            raise ErrorCode.DateExist()
        result = await self.crud.create(data)
        return result

    async def update(self, _id, data):
        result = await self.crud.update_by_id(_id, data)
        if not result:
            raise ErrorCode.InvalidBooking()
        return result

    async def get(self, _id):
        result = await self.crud.get_by_id(_id)
        if not result:
            raise ErrorCode.InvalidBooking()
        return result

    async def delete(self, _id):
        result = await self.crud.delete_by_id(_id)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.crud.search(query, page, limit)
        return result