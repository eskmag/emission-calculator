from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from main.api.api import router

# Emission Calculator API
app = FastAPI(
    title="Emission Calculator API",
    description="API for calculating carbon emissions based on user profiles and activities.",
    version="1.0.0"
)

# Include the API router
app.include_router(router, prefix="/api")

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods for development; restrict in production
    allow_headers=["*"],  # Allow all headers for development; restrict in production
)

# Mount the frontend static files
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

