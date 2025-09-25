from decimal import Decimal
from bson.decimal128 import Decimal128
from typing import List, Optional, Literal
from pydantic import BaseModel, validator


class InvoiceCreate(BaseModel):
    member_id: str
    artist_id: str
    start_time: float
    end_time: float
    status: Literal["pending", "confirmed", "cancelled"]
    cost: Optional[Decimal] = None
    location: Optional[str] = None
    notes: Optional[str] = None

    @validator('cost')
    def convert_decimal(cls, v):
        if isinstance(v, Decimal128):
            return v.to_decimal()
        return v

class InvoiceUpdate(BaseModel):
    member_id: Optional[str] = None
    artist_id: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    status: Optional[Literal["pending", "confirmed", "cancelled"]] = None
    cost: Optional[Decimal] = None
    location: Optional[str] = None
    notes: Optional[str] = None

    @validator('cost')
    def convert_decimal(cls, v):
        if isinstance(v, Decimal128):
            return v.to_decimal()
        return v


class InvoiceResponse(BaseModel):
    member_id: Optional[str] = None
    artist_id: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    status: Optional[Literal["pending", "confirmed", "cancelled"]] = None
    cost: Optional[Decimal] = None
    location: Optional[str] = None
    notes: Optional[str] = None

    @validator('cost')
    def convert_decimal(cls, v):
        if isinstance(v, Decimal128):
            return v.to_decimal()
        return v
    

class PaginatedInvoiceResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    results: List[InvoiceResponse]
