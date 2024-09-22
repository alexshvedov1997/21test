from fastapi import APIRouter, status
from schemas.posts import Posts, MlPostPredict
from ml.simple_ml import SimpleML

router = APIRouter()


@router.get(
    "/{title}",
    status_code=status.HTTP_200_OK,
    summary="Get Ml post",
    description="Endpoint for ml posts predict",
    response_model=MlPostPredict,
)
async def get_predict(
        title: str,
) -> MlPostPredict:
    ml_text = await SimpleML().predict(title)
    return MlPostPredict(
        ml_text=ml_text,
    )
