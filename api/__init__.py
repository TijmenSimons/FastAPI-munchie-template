from fastapi import APIRouter

from api.user.v1.user import user_v1_router
from api.auth.v1.auth import auth_v1_router
from api.recipe.v1.recipe import recipe_v1_router
from api.swipe_session.v1.swipe_session import swipe_session_v1_router
from api.swipe.v1.swipe import swipe_v1_router
from api.ingredient.v1.ingredient import ingredient_v1_router
from api.tag.v1.tag import tag_v1_router
from api.group.v1.group import group_v1_router
from api.image.v1.image import image_v1_router
from api.me.v1.me import me_v1_router

router = APIRouter()
router.include_router(me_v1_router, prefix="/me", tags=["Me"])
router.include_router(user_v1_router, prefix="/users", tags=["User"])
router.include_router(auth_v1_router, prefix="/auth", tags=["Auth"])
router.include_router(group_v1_router, prefix="/groups", tags=["Groups"])
router.include_router(swipe_session_v1_router, prefix="/swipe_sessions", tags=["Swipe Session"])
router.include_router(swipe_v1_router, prefix="/swipes", tags=["Swipe"])
router.include_router(recipe_v1_router, prefix="/recipes", tags=["Recipe"])
router.include_router(ingredient_v1_router, prefix="/ingredients", tags=["Ingredient"])
router.include_router(tag_v1_router, prefix="/tags", tags=["Tag"])
router.include_router(image_v1_router, prefix="/images", tags=["Image"])


__all__ = ["router"]
