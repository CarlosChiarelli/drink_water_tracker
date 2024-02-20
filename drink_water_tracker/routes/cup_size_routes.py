from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from drink_water_tracker.routes.deps import get_db_session
from drink_water_tracker.use_cases.cup_size import CupSizeUseCases

router = APIRouter(prefix="/cup-size", tags=["cup-size"])


@router.get("/list")
def list_cup_sizes(db_session: Session = Depends(get_db_session)):
    uc = CupSizeUseCases(db_session=db_session)
    response = uc.list_cup_sizes()

    return response
