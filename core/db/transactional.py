from functools import wraps

from core.db import session


class Transactional:
    def __call__(self, func):
        @wraps(func)
        async def _transactional(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                await session.commit()
            except Exception as exc:
                await session.rollback()
                raise exc

            return result

        return _transactional
