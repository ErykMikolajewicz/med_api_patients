from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Query
from asyncpg import Pool

from src.routers.account import token_authentication
from src.databases.relational import get_session
from src.services.specialist import get_specialists_list

router = APIRouter(tags=['specialists'], dependencies=[Depends(token_authentication)])

AsyncPool = Annotated[Pool, Depends(get_session)]
SpecialistType = Annotated[int | None, Query()]


@router.get("/specialists")
async def get_specialists(pool: AsyncPool, specialist_type_id: SpecialistType = None):
    async with pool.acquire() as session:
        specialists_list = await get_specialists_list(session, specialist_type_id)
    if not specialists_list:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    for specialist in specialists_list:
        specialist = dict(specialist)
        specialist['location'] = f"/specialists/{specialist['id']}"
    return specialists_list
