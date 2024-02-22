from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from drink_water_tracker.routes.deps import get_db_session
from drink_water_tracker.schemas.user import User
from drink_water_tracker.use_cases.user import UserUseCases

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/add", status_code=status.HTTP_201_CREATED, description="Add new user.")
def add_user(user: User, db_session: Session = Depends(get_db_session)):
    uc = UserUseCases(db_session=db_session)
    uc.add_user(user=user)
    return Response(status_code=status.HTTP_201_CREATED)
