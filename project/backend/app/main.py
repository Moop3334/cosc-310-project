from fastapi import FastAPI
from app.routers.restaurant_routers import router as restaurant_router, menu_router

app = FastAPI()

"""
Main app entry point for the Graveyard Shift backend.
"""

# ...rest of the code...
@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(restaurant_router)
app.include_router(menu_router)