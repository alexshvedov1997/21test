from abc import ABC, abstractmethod
from schemas.posts import Posts as PostSchema
from httpx import AsyncClient
from typing import List
import asyncio
from models.posts import Posts
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from db.postgres import get_session_service
from logging import getLogger

_logger = getLogger(__name__)


class BaseParser(ABC):

    @abstractmethod
    def parse_json(self, json_load: dict):
        ...


class BymykelApiParser(BaseParser):

    def parse_json(self, json_load: list) -> List[PostSchema]:
        result = []
        for post in json_load:
            result.append(
                PostSchema(
                    title=post.get("name"),
                    post_text=post.get("description"),
                )
            )
        return result


class HttpRequester:

    async def make_requests(self, url_: str, parser: BaseParser):
        async with AsyncClient() as client:
            response = await client.get(url=url_)
            response.raise_for_status()
            data_for_insert = parser.parse_json(response.json())
            session = await get_session_service()
            for post in data_for_insert:
                await self.upsert_record(session, post.dict(exclude_unset=True))
            return response

    async def upsert_record(self, session: AsyncSession, post: dict):
        statement = select(exists(Posts).where(Posts.title == post["title"]))
        is_post_exist = await session.execute(statement)
        is_post_exist = is_post_exist.scalar_one_or_none()
        if is_post_exist:
            return
        post_id = Posts(
            **post,
        )
        session.add(post_id)
        await session.commit()

    async def run_process(self):
        urls = [
            "https://bymykel.github.io/CSGO-API/api/ru/skins.json",
            "https://bymykel.github.io/CSGO-API/api/ru/stickers.json",
            "https://bymykel.github.io/CSGO-API/api/ru/collectibles.json",
            "https://bymykel.github.io/CSGO-API/api/ru/agents.json",
        ]
        tasks = [asyncio.create_task(self.make_requests(url_, BymykelApiParser())) for url_ in urls]
        for complete_task in asyncio.as_completed(tasks):
            try:
                res = await complete_task
            except Exception as error:
                _logger.error(f"Exception in task {error}")

