from fastapi import FastAPI
from main.api.api import router

app = FastAPI(
    title="Emission Calculator API",
    description="API for calculating carbon emissions based on user profiles and activities.",
    version="1.0.0"
)

app.include_router(router, prefix="/api")