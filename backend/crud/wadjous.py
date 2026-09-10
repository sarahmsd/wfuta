from sqlalchemy.exc import SQLAlchemyError
from schemas.wadjouCreation import WadjouCreation
from schemas.wadjouMaj import WadjouMaj
from sqlalchemy.orm import Session
from models.wadjous import Wadjou
from models.cheikhs import Cheikh

def create_wadjou(cheikh_id : int, w : WadjouCreation, db : Session):
    try:
        db_wadjou = Wadjou(
            libelle = w.libelle,
            medialink = w.medialink,
            dateCreation = w.dateCreation,
            dateMaj = w.dateMaj,
            id_cheikh = cheikh_id
        )

        db.add(db_wadjou)
        db.commit()
        db.refresh(db_wadjou)

        return db_wadjou
    except SQLAlchemyError as e:
        db.rollback()
        raise


def update_wadjou(id : int, w : WadjouMaj, db : Session):
    try:
        #Get the wadjou from the database
        db_wadjou = db.query(Wadjou).filter(Wadjou.id == id).first()
        if not db_wadjou:
            return None

        #Fill in the columns with the values
        for cle, valeur in w.dict(exclude_unset=True).items():
            setattr(db_wadjou, cle, valeur)

        db.commit()
        db.refresh(db_wadjou)

        return db_wadjou
    except SQLAlchemyError as e:
        db.rollback()
        raise


def get_all_wadjous(cheikh_id : int, db : Session):
    try:
        db_wadjous = db.query(Wadjou).filter(Wadjou.id_cheikh == cheikh_id)
        return db_wadjous
    except SQLAlchemyError:
        raise


def get_last_wadjou(cheikh_id : int, db : Session):
    try:
        db_wadjou = db.query(Wadjou).filter(Wadjou.id_cheikh == cheikh_id).order_by(
            Wadjou.dateCreation.desc(),
            Wadjou.id.desc()
        ).limit(4).all()
        return db_wadjou
    except SQLAlchemyError:
        raise


def get_wadjou(id : int, db : Session):
    try:
        db_wadjou = db.query(Wadjou).filter(Wadjou.id == id).first()
        return db_wadjou
    except SQLAlchemyError:
        raise


def delete_wadjou(id : int, db : Session):
    try:
        db_wadjou = db.query(Wadjou).filter(Wadjou.id == id).first()

        if not db_wadjou:
            return None

        db.delete(db_wadjou)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise    
 