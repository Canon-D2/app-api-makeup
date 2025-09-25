from fastapi import APIRouter, Query, Path
from . import schemas
from .controllers import UserController
from typing import Optional

router = APIRouter(prefix="/v1/user", tags=["user"])
controller = UserController()


@router.post("/create", status_code=201, responses={
                201: {"model": schemas.UserResponse, "description": "Create items success"}})
async def create_user(data: schemas.UserCreate):
    result = await controller.create(data.model_dump())
    return schemas.UserResponse(**result)


@router.get("/get/{user_id}", status_code=200, responses={
                200: {"model": schemas.UserResponse, "description": "Get items success"}})
async def get_user(user_id: str = Path(...)):
    result = await controller.get(user_id)
    return result


@router.put("/edit/{user_id}", status_code=200, responses={
                200: {"model": schemas.UserResponse, "description": "Edit items success"}})
async def update_user(user_id: str, data: schemas.UserUpdate):
    result = await controller.update(user_id, data.model_dump(exclude_unset=True))
    return schemas.UserResponse(**result)


@router.delete("/delete/{user_id}", status_code=200, responses={
                200: {"description": "Delete items success"}})
async def delete_user(user_id: str):
    result = await controller.delete(user_id)
    return result


@router.get("/search", status_code=200, responses={
                200: {"model": schemas.PaginatedUserResponse, "description": "Get items success"}})
async def list_users(
    page: int = Query(1, gt=0),
    limit: int = Query(10, le=100),
    search: Optional[str] = None,
):
    query = {}
    if search:
        query["$or"] = [
            {"email": {"$regex": search, "$options": "i"}},
            {"phone": {"$regex": search, "$options": "i"}},
        ]
    result = await controller.search(query, page, limit)
    return result
