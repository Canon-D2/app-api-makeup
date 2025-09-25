from fastapi import APIRouter, Query
from . import schemas
from typing import Optional
from .controllers import BookingController

router = APIRouter(prefix="/v1/booking", tags=["booking"])
controller = BookingController()


@router.post("/create", status_code=201, responses={
                201: {"model": schemas.BookingResponse, "description": "Create items success"}})
async def create_booking(data: schemas.BookingCreate):
    result = await controller.create(data.model_dump())
    return schemas.BookingResponse(**result)

@router.get("/get/{booking_id}", status_code=200, responses={
                200: {"model": schemas.BookingResponse, "description": "Get items success"}})
async def get_booking(booking_id: str):
    result = await controller.get(booking_id)
    return result

@router.put("/edit/{booking_id}", status_code=200, responses={
                200: {"model": schemas.BookingResponse, "description": "Edit items success"}})
async def update_booking(booking_id: str, data: schemas.BookingUpdate):
    result = await controller.update(booking_id, data.model_dump(exclude_unset=True))
    return schemas.BookingResponse(**result)

@router.delete("/delete/{booking_id}", status_code=200, responses={
                200: {"description": "Delete items success"}})
async def delete_booking(booking_id: str):
    result = await controller.delete(booking_id)
    return result

@router.get("/search", status_code=200, responses={
                200: {"model": schemas.PaginatedBookingResponse, "description": "Get items success"}})
async def list_booking(
    page: int = Query(1, gt=0, description="Số trang"),
    limit: int = Query(10, le=100, description="Số item / mỗi trang"),
    date: Optional[str] = Query(None, description="Tìm theo tên"),
):
    query = {}
    if date: query["date"] = {"$regex": date, "$options": "i"}

    result = await controller.search(query, page, limit)
    return result
