from fastapi import FastAPI
from app.routers.restaurant_routers import router as items_router

app = FastAPI()

"""
Main app entry point for the Graveyard Shift backend.
"""

# ...rest of the code...
@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(items_router)
