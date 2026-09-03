from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from config import settings
from core.database import engine, Base
from routes import auth_router

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        openapi_version="3.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        debug=settings.DEBUG,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _register_routes(app)

    return app

def _register_routes(app: FastAPI) -> None:
    """Register all API routes with the FastAPI application."""

    @app.get("/")
    def root() -> dict[str, str]:
        """Root endpoint to check if the API is running."""
        return {
            "app": settings.APP_NAME,
            "version": settings.VERSION,
            "status": "healthy",
        }

    @app.get("/health")
    def health_check() -> dict[str, str]:
        """Health check endpoint to verify the API is running."""
        return {"status": "healthy"}

    app.include_router(auth_router)
