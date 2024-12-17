from fastapi import FastAPI

from app.routes import books, borrow, health_check, users

# Initialize FastAPI app
app = FastAPI(
    title="E-Library API System",
    description="API for managing an online library system",
)

# Include routers
app.include_router(health_check.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(borrow.router)
