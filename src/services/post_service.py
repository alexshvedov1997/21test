import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from models.posts import Posts
from schemas.posts import Posts as PostsSchema
from core import exceptions
from services.cache_service import CacheService
from db import redis

_logger = logging.getLogger(__name__)


class PostService:

    async def get_post_by_id(self, id_post: int, session: AsyncSession) -> PostsSchema:
        cache_service = CacheService(redis.redis)
        post_key = f"post-{id_post}"
        post_dict = await cache_service.get_value(post_key)
        if post_dict:
            return PostsSchema(**post_dict)
        statement = select(Posts).where(Posts.id == id_post).limit(1)
        post_id = await session.execute(statement)
        post_id = post_id.scalar_one_or_none()
        if not post_id:
            _logger.error(f"Post with id {id_post} doesn't exist in db")
            raise exceptions.PostNotFound
        post_schema = PostsSchema(
            id=post_id.id,
            title=post_id.title,
            post_text=post_id.post_text,
        )
        await cache_service.set_value(post_key, post_schema.dict())
        return post_schema

    async def create_post(self, input_data: PostsSchema, session: AsyncSession) -> PostsSchema:
        statement = select(exists(Posts).where(Posts.title == input_data.title))
        is_post_exist = await session.execute(statement)
        is_post_exist = is_post_exist.scalar_one_or_none()
        if is_post_exist:
            _logger.error(f"Post with title {input_data.title} already exist")
            raise exceptions.PostAlreadyExist
        post_id = Posts(
            **input_data.dict(exclude_unset=True),
        )
        session.add(post_id)
        await session.commit()
        return PostsSchema(
            id=post_id.id,
            title=post_id.title,
            post_text=post_id.post_text,
        )
