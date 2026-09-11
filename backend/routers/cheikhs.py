from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from crud.cheikhs import create_cheikh
from db.database import get_db
from schemas.cheikhCreation import CheikhCreation


router = APIRouter(prefix="/cheikhs", tags=["Cheikhs"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_cheikh_endpoint(cheikh: CheikhCreation, db: Session = Depends(get_db)):
    try:
        return create_cheikh(cheikh, db)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur interne") from error
