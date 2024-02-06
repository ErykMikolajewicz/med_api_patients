from typing import Any, Annotated
from uuid import UUID
from datetime import date

from fastapi import APIRouter, Depends, Response, Request, status, HTTPException, Query
from asyncpg import Pool

import src.services.messages as srv_message
from src.routers.account import token_authentication
from src.domain.models.messages import Message
from src.databases.relational import get_session
from src.services.general import prepare_pagination_link
from src.domain.models.general import pagination_dependency


router = APIRouter(tags=['messages'], dependencies=[Depends(token_authentication)])

AsyncPool = Annotated[Pool, Depends(get_session)]
DateQuery = Annotated[date | None, Query()]


@router.get('/messages')
async def get_my_messages(session: AsyncPool, pagination: pagination_dependency, response: Response, request: Request,
                          specialist_id: UUID = None, messages_from: DateQuery = None, messages_to: DateQuery = None):
    patient_id = request.state.patient_id
    async with session.acquire() as session:
        messages, messages_number = await srv_message.get_list(session, patient_id, specialist_id, messages_from,
                                                               messages_to)
    if not messages:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    for message in messages:
        message = dict(message)
        message['location'] = f'/messages/my/{message["id"]}'
    link_base = '<messages?page-number={0}&page-size={1}>; {2}'
    links = prepare_pagination_link(link_base, pagination, messages_number)
    response.headers['Link'] = links
    return messages


@router.get('/messages/{message_id}')
async def get_my_message(message_id: UUID, session: AsyncPool, response: Response, request: Request):
    patient_id = request.state.patient_id
    async with session.acquire() as session:
        message = await srv_message.get(session, patient_id, message_id)
    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    response.headers['Location'] = f'/messages/my/{message["id"]}'
    return message


@router.post('/messages', status_code=status.HTTP_201_CREATED)
async def add_message(message: Message, session: AsyncPool, response: Response, request: Request):
    patient_id = request.state.patient_id
    message: dict[str, Any] = message.model_dump()
    message['patient_id'] = patient_id
    async with session.acquire() as session:
        new_message = await srv_message.add(session, message)
    message_id = new_message['id']
    response.headers['Location'] = f'/messages/my/{message_id}'
    return new_message
