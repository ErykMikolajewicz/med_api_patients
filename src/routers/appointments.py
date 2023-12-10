from fastapi import APIRouter, Depends

from src.routers.account import token_authentication

router = APIRouter(tags=['appointments'], dependencies=[Depends(token_authentication)])


@router.post("/appointments")
async def add_appointment():
    pass
