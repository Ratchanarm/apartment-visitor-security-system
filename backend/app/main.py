from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, visitors, deliveries, emergency, apartments
from app.config import get_settings

settings = get_settings()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Apartment Security System",
    description="Digital visitor management and security system",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(visitors.router)
app.include_router(deliveries.router)
app.include_router(emergency.router)
app.include_router(apartments.router)


@app.get("/")
async def root():
    return {"message": "Apartment Security API", "docs": "/docs"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
