from typing import Optional,TypeVar

from pydantic import BaseModel

T = TypeVar('T')

class ResponseData(BaseModel):
    code: int = 200
    detail: str
    result: Optional[T] = None