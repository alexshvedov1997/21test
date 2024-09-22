from db.postgres import get_session
from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.posts import Posts
from services.post_service import PostService
from core.error_handlers import HttpErrorHandler
from ml.simple_ml import SimpleML

router = APIRouter()


@router.get(
    "/{post_id}",
    status_code=status.HTTP_200_OK,
    summary="Get Post",
    description="Endpoint to get list of posts",
    response_model=Posts,

)
async def get_posts(
        post_id: int,
        db: AsyncSession = Depends(get_session),
) -> Posts:
    # await SimpleML().train_by_bd()
    # res = await SimpleML().predict("reter")
    async with HttpErrorHandler():
        result = await PostService().get_post_by_id(post_id, db)
        return result


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create Post",
    description="Endpoint to create of post",
    response_model=Posts,
)
async def create_posts(
        input_data: Posts = Body(...),
        db: AsyncSession = Depends(get_session),
) -> Posts:
    async with HttpErrorHandler():
        result = await PostService().create_post(input_data, db)
        return result
