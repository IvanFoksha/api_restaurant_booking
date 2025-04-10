from fastapi import APIRouter

from app.api.v1.endpoints import tables, reservations

api_router = APIRouter()

# Include routers for different endpoints
api_router.include_router(
    tables.router,
    prefix="/tables",
    tags=["tables"]
)

api_router.include_router(
    reservations.router,
    prefix="/reservations",
    tags=["reservations"]
) 