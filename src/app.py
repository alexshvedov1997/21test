from logging import config as logging_config
import aioredis

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from db import redis

from core.config import settings
from core.logger import LOGGING
from api.v1 import posts, ml_api
from connectors import faststream_con
from faststream.redis import RedisBroker
from faststream import FastStream
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_faststream import BrokerWrapper, StreamScheduler
from faststream_tasks.store_data import base_handler, fill_ml

logging_config.dictConfig(LOGGING)


app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

faststream_con.broker = RedisBroker(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0')
faststream_app = FastStream(faststream_con.broker)

taskiq_broker = BrokerWrapper(faststream_con.broker)


taskiq_broker.task(
    message=base_handler,
    channel="queue",
    schedule=[{
        "cron": "0 0 */12 * *"
    }],
)
taskiq_broker.task(
    message=fill_ml,
    channel="queue",
    schedule=[{
        "cron": "0 0 * * *"
    }],
)

scheduler = StreamScheduler(
    broker=taskiq_broker,
    sources=[LabelScheduleSource(taskiq_broker)],
)


@app.on_event("startup")
async def startup():
    redis.redis = await aioredis.create_redis_pool(
        (settings.REDIS_HOST, settings.REDIS_PORT),
        minsize=10,
        maxsize=20,
        db=1,
    )


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()

app.include_router(posts.router, prefix="/api/v1/posts", tags=["posts"])
app.include_router(ml_api.router, prefix="/api/v1/ml", tags=["ml"])


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
    )

#airflow-apache и sky-lern