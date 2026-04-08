from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.restaurant_routers import router as restaurant_router, menu_router
from app.routers.order_routers import router as order_router
from app.routers.payment_routers import router as payment_router
from app.routers.user_routers import router as user_router
from app.routers.cart_routers import router as cart_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
Main app entry point for the Graveyard Shift backend.
"""

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(restaurant_router)
app.include_router(menu_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(user_router)
app.include_router(cart_router)
