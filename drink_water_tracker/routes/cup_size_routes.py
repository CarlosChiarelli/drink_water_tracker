from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from drink_water_tracker.routes.deps import get_db_session
from drink_water_tracker.schemas.cup_size import CupSize, CupSizeOutput
from drink_water_tracker.use_cases.cup_size import CupSizeUseCases

router = APIRouter(prefix="/cup-size", tags=["Cup size"])


@router.post("/add", status_code=status.HTTP_201_CREATED, description="Add new cup size.")
def add_cup_size(cup_size: CupSize, db_session: Session = Depends(get_db_session)):
    uc = CupSizeUseCases(db_session=db_session)
    uc.add_cup_size(cup_size=cup_size)
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/list", response_model=List[CupSizeOutput], description="List cup sizes.")
def list_cup_sizes(db_session: Session = Depends(get_db_session)):
    uc = CupSizeUseCases(db_session=db_session)
    response = uc.list_cup_sizes()

    return response
