from .auth import router as auth_router
from .users import router as users_router
from .general import router as general_router

__all__ = ["auth_router", "users_router", "general_router"]