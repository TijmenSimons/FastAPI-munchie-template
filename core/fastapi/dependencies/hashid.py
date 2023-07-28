import json
from fastapi import Path, Request

from core.helpers.hashid import decode_single


async def get_path_group_id(group_id: str = Path(...)):
    return decode_single(group_id)

async def get_path_session_id(session_id: str = Path(...)):
    return decode_single(session_id)

async def get_path_user_id(user_id: str = Path(...)):
    return decode_single(user_id)
