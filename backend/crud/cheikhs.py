from sqlalchemy.exc import SQLAlchemyError
from schemas.cheikhCreation import CheikhCreation
from schemas.cheikhMaj import CheikhMaj
from sqlalchemy.orm import Session
from models.cheikhs import Cheikh

from .medias import get_portrait_by_entity



def create_cheikh(c : CheikhCreation, db : Session):
    try:
        db_cheikh = Cheikh(
            nom = c.nom,
            prenom = c.prenom,
            bio = c.bio,
            foyer = c.foyer,
            dateCreation = c.dateCreation,
            dateMaj = c.dateMaj
        )

        db.add(db_cheikh)
        db.commit()
        db.refresh(db_cheikh)

        return db_cheikh
    except SQLAlchemyError as e:
        db.rollback()
        raise


def update_cheikh(id : int, c : CheikhMaj, db : Session):
    try:
        #Get the cheikh from the database
        db_cheikh = db.query(Cheikh).filter(Cheikh.id == id).first()
        if not db_cheikh:
            return None

        #Fill in the columns with the values
        for cle, valeur in c.dict(exclude_unset=True).items():
            setattr(db_cheikh, cle, valeur)

        db.commit()
        db.refresh(db_cheikh)

        return db_cheikh
    except SQLAlchemyError as e:
        db.rollback()
        raise


def get_all_cheikhs(db : Session):
    try:
        db_cheikhs = db.query(Cheikh).all()

        for cheikh in db_cheikhs:
            result = get_portrait_by_entity(db, "cheikh", cheikh.id, "portrait")
            if not result :
                cheikh.portrait = "/media-files/photos/default-portrait.jpg"
            else : 
                cheikh.portrait =  f"/media-files/{result.chemin}"

        return db_cheikhs
    
    except SQLAlchemyError:
        raise


def get_last_cheikh(db : Session):
    try:
        db_cheikh = db.query(Cheikh).order_by(
            Cheikh.dateCreation.desc(),
            Cheikh.id.desc()
        ).limit(3).all()


        for cheikh in db_cheikh:
            result = get_portrait_by_entity(db, "cheikh", cheikh.id, "portrait")
            if not result :
                cheikh.portrait = "/media-files/photos/default-portrait.jpg"
            else : 
                cheikh.portrait =  f"/media-files/{result.chemin}"

        return db_cheikh
    except SQLAlchemyError:
        raise


def get_cheikh(id : int, db : Session):
    try:
        db_cheikh = db.query(Cheikh).filter(Cheikh.id == id).first()
        return db_cheikh
    except SQLAlchemyError:
        raise


def delete_cheikh(id : int, db : Session):
    try:
        db_cheikh = db.query(Cheikh).filter(Cheikh.id == id).first()

        if not db_cheikh:
            return None

        db.delete(db_cheikh)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise    
    