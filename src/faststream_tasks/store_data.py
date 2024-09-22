from services.http_requester import HttpRequester
from ml.simple_ml import SimpleML


async def base_handler():
    await HttpRequester().run_process()


async def fill_ml():
    await SimpleML().train_by_bd()
