"""
Finalytics MVP Platform - Main Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import routers
from app.routers import auth, documents, news, exports, stocks, comparison

app = FastAPI(
    title="Finalytics MVP Platform",
    description="Financial analytics platform with AI-powered document intelligence",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "Finalytics MVP"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - serves the frontend UI"""
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(news.router, prefix="/api/news", tags=["news"])
app.include_router(exports.router, prefix="/api/exports", tags=["exports"])
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])
app.include_router(comparison.router, prefix="/api/comparison", tags=["comparison"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

