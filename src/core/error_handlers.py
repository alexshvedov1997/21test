from fastapi import status, HTTPException
from core.exceptions import PostNotFound, PostAlreadyExist
import logging
from functools import wraps

_logger = logging.getLogger(__name__)


class HttpErrorHandler:

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            if issubclass(exc_type, PostAlreadyExist):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Post already exist",
                )
            elif issubclass(exc_type, PostNotFound):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found",
                )
            else:
                _logger.error(
                    f"Error in controller: {exc_type} \n {exc_val} \n {exc_tb}"
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Internal server error: {exc_type} \n {exc_val}",
                )
            return True
        return False


def http_error_loger(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except:
            pass
    return wrapper

