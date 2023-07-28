from enum import Enum


class BaseEnum(Enum):
    pass


class UserEnum(BaseEnum):
    pass


class WebsocketActionEnum(str, BaseEnum):
    CONNECTION_CODE = "CONNECTION_CODE"
    POOL_MESSAGE = "POOL_MESSAGE"
    GLOBAL_MESSAGE = "GLOBAL_MESSAGE"


class SwipeSessionActionEnum(str, BaseEnum):
    # When editing this, edit app\swipe_session\services\action_docs.py too
    CONNECTION_CODE = "CONNECTION_CODE"
    RECIPE_MATCH = "RECIPE_MATCH"
    POOL_MESSAGE = "POOL_MESSAGE"
    GLOBAL_MESSAGE = "GLOBAL_MESSAGE"
    RECIPE_SWIPE = "RECIPE_SWIPE"
    SESSION_STATUS_UPDATE = "SESSION_STATUS_UPDATE"
    GET_RECIPES = "GET_RECIPES"


class SwipeSessionEnum(str, BaseEnum):
    CANCELLED = "Gestopt"
    COMPLETED = "Voltooid"
    IN_PROGRESS = "Is bezig"
    PAUSED = "Gepauzeerd"
    READY = "Staat klaar"

class TagType(str, BaseEnum):
    ALLERGIES = "Allergieën"
    CUISINE = "Keuken"
    DIET = "Dieet"

