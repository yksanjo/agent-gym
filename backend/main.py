from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import logging
from typing import Optional

from database import engine, Base
from config import settings
from middleware import LoggingMiddleware
from api import agents, feedback, ab_testing, fine_tuning, synthetic_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Agent Gym API")
    
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Agent Gym API")

app = FastAPI(
    title="Agent Gym API",
    description="Training environments for AI agents",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(feedback.router, prefix="/api/v1/feedback", tags=["feedback"])
app.include_router(ab_testing.router, prefix="/api/v1/ab-testing", tags=["ab-testing"])
app.include_router(fine_tuning.router, prefix="/api/v1/fine-tuning", tags=["fine-tuning"])
app.include_router(synthetic_data.router, prefix="/api/v1/synthetic-data", tags=["synthetic-data"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Agent Gym API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "agent-gym-api",
        "timestamp": "2024-01-20T23:15:00Z"
    }

@app.get("/api/v1/status")
async def api_status():
    return {
        "api": "running",
        "version": "0.1.0",
        "features": {
            "feedback_collection": True,
            "ab_testing": True,
            "fine_tuning": True,
            "synthetic_data": True
        }
    }

# Dependency for authentication
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    # TODO: Implement proper authentication
    # For now, return a mock user
    token = credentials.credentials
    return {
        "id": "user_123",
        "email": "demo@agentgym.ai",
        "role": "admin"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )