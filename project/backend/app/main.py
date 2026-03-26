from fastapi import FastAPI
from app.routers.restaurant_routers import router as restaurant_router, menu_router
from app.routers.order_routers import router as order_router
from app.routers.payment_routers import router as payment_router
from app.routers.user_routers import router as user_router

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
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(user_router)
