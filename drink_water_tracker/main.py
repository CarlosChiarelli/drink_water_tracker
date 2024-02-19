from fastapi import FastAPI

from drink_water_tracker.routes.user_routes import router as user_routes

app = FastAPI()


@app.get("/health-check")
def health_check() -> bool:
    return True


app.include_router(user_routes)
