from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/")
def index():
    return PlainTextResponse(status_code=418)
