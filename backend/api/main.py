from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import API_HOST, API_PORT, ALLOWED_ORIGINS
from backend.api.dependencies import get_db

# Import bundle routers
from backend.bundles.geo_locations.api.router import router as geo_location_router
from backend.bundles.users.api.router import router as user_router
from backend.bundles.incidents.api.router import router as incident_router
from backend.bundles.notifications.api.router import router as notification_router
from backend.bundles.profiles.api.router import router as profile_router
from backend.bundles.config.api.router import router as config_router

# Import scheduler
from backend.core.scheduler import start_scheduler

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="NOTI Backend API",
        description="Backend API for NOTI - Power Outage Notification System",
        version="1.0.0"
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers with prefixes
    app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
    app.include_router(geo_location_router, prefix="/api/v1/locations", tags=["Locations"])
    app.include_router(incident_router, prefix="/api/v1/incidents", tags=["Incidents"])
    app.include_router(notification_router, prefix="/api/v1/notifications", tags=["Notifications"])
    app.include_router(profile_router, prefix="/api/v1/profiles", tags=["Profiles"])
    app.include_router(config_router, prefix="/api/v1/config", tags=["Configuration"])

    # Health check endpoints
    @app.get("/")
    def root():
        return {"message": "NOTI Backend API funcionando correctamente"}

    @app.get("/health")
    def health_check():
        return {"status": "healthy", "service": "backend"}

    # Startup event
    @app.on_event("startup")
    async def startup_event():
        print("🚀 Iniciando servidor FastAPI Backend...")
        start_scheduler()

    return app

# Create the app instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
