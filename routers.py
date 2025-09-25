from fastapi import APIRouter

from apps.modules.home.routers import router as home_router
from apps.modules.user.routers import router as user_router
from apps.modules.booking.routers import router as booking_router
from apps.modules.account.router import router as account_router
from apps.modules.invoices.routers import router as invoice_router

api_router = APIRouter()

api_router.include_router(home_router)
api_router.include_router(user_router)
api_router.include_router(booking_router)
api_router.include_router(account_router)
api_router.include_router(invoice_router)