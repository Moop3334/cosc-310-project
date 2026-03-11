from fastapi import APIRouter

from .routers import router

# package-level router object that can be included in main application
__all__ = ["router"]
