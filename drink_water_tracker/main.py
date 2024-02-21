from fastapi import FastAPI

from drink_water_tracker.routes.cup_size_routes import router as cup_size_routes
from drink_water_tracker.routes.user_routes import router as user_routes
from drink_water_tracker.routes.water_consumption_routes import (
    router as water_consumption_routes,
)

app = FastAPI()


@app.get("/health-check")
def health_check() -> bool:
    return True


app.include_router(user_routes)
app.include_router(cup_size_routes)
app.include_router(water_consumption_routes)
