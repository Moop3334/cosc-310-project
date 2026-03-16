from fastapi import APIRouter

from .restaurant_routers import router

# package-level router object that can be included in main application
__all__ = ["router"]
