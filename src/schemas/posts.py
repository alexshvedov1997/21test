from pydantic import BaseModel
from typing import Optional


class Posts(BaseModel):
    id: Optional[int]
    title: str
    post_text: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "title",
                "post_text": "post_text",
            }
        }


class MlPostPredict(BaseModel):
    ml_text: str
