from core.helpers.hashid import decode, decode_single, encode


class HashId(int):
    """Pydantic type for hashing integer"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, int):
            raise TypeError('integer required')        
        return encode(v)
    

class DehashId(str):
    """Pydantic type for dehashing hash"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            try: 
                int(v)
                return v
            except:
                raise TypeError('hash required')
        
        return decode_single(v)
        