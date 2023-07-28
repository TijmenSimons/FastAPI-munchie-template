from app.image.interface.image import ObjectStorageInterface, AzureBlobInterface
from core.config import config


async def get_object_storage() -> ObjectStorageInterface:
    if config.OBJECT_STORAGE_INTERFACE == "azure":
        return AzureBlobInterface
    else:
        raise NotImplementedError(
            f"The {config.OBJECT_STORAGE_INTERFACE} object storage interface is not implemented"
        )
