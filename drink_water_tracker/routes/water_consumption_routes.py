from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from drink_water_tracker.routes.deps import get_db_session
from drink_water_tracker.schemas.water_consumption import (
    WaterConsumptionInput,
    WaterConsumptionOutput,
)
from drink_water_tracker.use_cases.water_consumption import WaterConsumptionUseCases

router = APIRouter(prefix="/water-consumption", tags=["Water consumption"])


@router.post(
    "/add", status_code=status.HTTP_201_CREATED, description="Add new water consumption."
)
def add_water_consumption(
    water_consumption_input: WaterConsumptionInput,
    db_session: Session = Depends(get_db_session),
):
    uc = WaterConsumptionUseCases(db_session=db_session)
    uc.add_water_consumption(
        water_consumption=water_consumption_input.water_consumption,
        user_id=water_consumption_input.user_id,
        cup_size_id=water_consumption_input.cup_size_id,
    )

    return Response(status_code=status.HTTP_201_CREATED)


@router.get(
    "/list",
    response_model=List[WaterConsumptionOutput],
    description="List water consumption.",
)
def list_water_consumption(
    username: str = "",
    drinkdate: date = date.today(),
    db_session: Session = Depends(get_db_session),
):
    uc = WaterConsumptionUseCases(db_session=db_session)
    water_consumption = uc.list_water_consumption(
        user_name=username, drink_date=drinkdate
    )

    return water_consumption


@router.get(
    "/list/all",
    response_model=List[WaterConsumptionOutput],
    description="List user's water consumption history.",
)
def list_all_water_consumption(
    username: str = "", db_session: Session = Depends(get_db_session)
):
    uc = WaterConsumptionUseCases(db_session=db_session)
    water_consumption = uc.list_water_consumption(user_name=username)

    return water_consumption
