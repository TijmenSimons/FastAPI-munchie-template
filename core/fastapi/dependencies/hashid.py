from fastapi import Path
from core.helpers.hashid import decode_single


async def get_path_user_id(user_id: str = Path(...)):
    return decode_single(user_id)
