from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path

from .routes import router

app = FastAPI(
    title="Resume Magic Writer API",
    description="AI-powered resume optimization and generation",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

project_root = Path(__file__).parent.parent.parent.parent
static_path = project_root / "static"

if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

    @app.get("/")
    async def serve_frontend():
        """Serve the frontend HTML"""
        index_path = static_path / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        return {"message": "Frontend not found. Please create static/index.html"}
else:
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": "Resume Magic Writer API",
            "docs": "/docs",
            "health": "/health",
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
