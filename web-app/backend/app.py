from fastapi import FastAPI
from auth import router as auth_router
from routers.protected import router as protected_router

# Initialize FastAPI
app = FastAPI()

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])  # Public routes
app.include_router(protected_router, prefix="/protected", tags=["Protected"])  # Protected routes

@app.get("/")
def read_root():
    """Public root endpoint for API health check."""
    return {"message": "Welcome to the FastAPI service for Elasticsearch!"}
