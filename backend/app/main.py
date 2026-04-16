"""
HausaAI Backend - FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database.connection import init_db, close_db
from app.routes import auth, translation, user

# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting HausaAI Backend...")
    await init_db()
    yield
    # Shutdown
    print("🛑 Shutting down HausaAI Backend...")
    await close_db()

# Initialize FastAPI app
app = FastAPI(
    title="HausaAI API",
    description="Intelligent Hausa Language Translation Platform",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Trusted Hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(translation.router, prefix="/api/translate", tags=["Translation"])
app.include_router(user.router, prefix="/api/user", tags=["User"])

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Check if the API is running"""
    return {"status": "✅ HausaAI Backend is running", "version": "1.0.0"}

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to HausaAI API",
        "docs": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
