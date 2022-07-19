from typing import List

from fastapi import APIRouter, Depends, Query

from app.user.schemas import (
    ExceptionResponseSchema,
    GetUserListResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema,
)
from app.user.services import UserService
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin,
)

user_router = APIRouter()


@user_router.get(
    "",
    response_model=List[GetUserListResponseSchema],  # https://fastapi.tiangolo.com/tutorial/response-model/#response-model
    response_model_exclude={"id"},  # https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude
    responses={"400": {"model": ExceptionResponseSchema}},  # https://fastapi.tiangolo.com/advanced/additional-responses/#additional-response-with-model
    dependencies=[Depends(PermissionDependency([IsAdmin]))],  # https://fastapi.tiangolo.com/tutorial/security/first-steps/#use-it
)
async def get_user_list(
    limit: int = Query(10, description="Limit"),
    prev: int = Query(None, description="Prev ID"),
):
    return await UserService().get_user_list(limit=limit, prev=prev)


@user_router.post(
    "",
    response_model=CreateUserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def create_user(request: CreateUserRequestSchema):
    await UserService().create_user(**request.dict())
    return {"email": request.email, "nickname": request.nickname}
