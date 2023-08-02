# Taken from https://pypi.org/project/fastapi-versioning/
# Edited because I want "/api" in front of "/latest"

from .versioning import VersionedFastAPI, version

__all__ = [
    "VersionedFastAPI",
    "version",
]
