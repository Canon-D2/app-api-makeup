from pydantic import BaseModel, Field
from typing import List, Optional

class TimeSlot(BaseModel):
    start_free: float 
    end_free: float


class BookingCreate(BaseModel):
    artist_id: str
    date: str
    freetime: List[TimeSlot]
    description: Optional[str] = None


class BookingUpdate(BaseModel):
    artist_id: Optional[str] = None
    date: Optional[str] = None
    freetime: Optional[List[TimeSlot]] = None
    description: Optional[str] = None


class BookingResponse(BaseModel):
    id: str = Field(alias="_id")
    artist_id: str
    date: Optional[str] = None
    freetime: Optional[List[TimeSlot]] = None
    description: Optional[str] = None
    created_at: float
    updated_at: Optional[float] = None


class PaginatedBookingResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    results: List[BookingResponse]
