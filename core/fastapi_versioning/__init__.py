# Taken from https://pypi.org/project/fastapi-versioning/
# Edited because I want "/api" in front of "/latest"

from .routing import versioned_api_route
from .versioning import VersionedFastAPI, version

__all__ = [
    "VersionedFastAPI",
    "versioned_api_route",
    "version",
]
