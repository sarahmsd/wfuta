from sqlalchemy.orm import Session
from models.medias import Media
from models.media_asso import MediaAsso
from schemas.mediaAssoCreation import MediaAssoCreation
from datetime import date
from sqlalchemy.exc import SQLAlchemyError

from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_DIR = BASE_DIR / "storage" / "media"


def create_media(db: Session, media_data: dict):
    try:
        db_media = Media(**media_data)
        
        db.add(db_media)
        db.commit()
        db.refresh(db_media)
    
        return db_media
    except SQLAlchemyError as e:
        db.rollback()
        raise


def save_media_file(file: UploadFile, media_type: str):
    # Déterminer le dossier selon le type de média
    folders = {
        "photo": "photos",
        "audio": "audios",
        "video": "videos"
    }

    folder = folders.get(media_type)

    if folder is None:
        raise ValueError("Type de média invalide")

    # Créer le dossier s'il n'existe pas
    destination_dir = MEDIA_DIR / folder
    destination_dir.mkdir(parents=True, exist_ok=True)

    # Récupérer l'extension du fichier original
    extension = Path(file.filename).suffix

    # Générer un nom unique
    filename = f"{uuid4()}{extension}"

    # Chemin physique du fichier
    destination = destination_dir / filename

    # Sauvegarder le fichier
    with destination.open("wb") as buffer:
        buffer.write(file.file.read())

    # Chemin relatif qui sera enregistré en BDD
    relative_path = f"{folder}/{filename}"

    return {
        "nom": file.filename,
        "chemin": relative_path,
        "type": media_type,
        "mime_type": file.content_type,
        "taille": destination.stat().st_size,
        "dateCreation": date.today(),
        "dateMaj": date.today()
    }


def create_media_association(
    db: Session,
    media_id: int,
    association_data: MediaAssoCreation
):
    db_association = MediaAsso(
        media_id=media_id,
        entity_type=association_data.entity_type,
        entity_id=association_data.entity_id,
        role=association_data.role
    )

    db.add(db_association)
    db.commit()
    db.refresh(db_association)

    return db_association


def get_media_by_entity(
    db: Session,
    entity_type: str,
    entity_id: int
):
    return (
        db.query(Media, MediaAsso.role)
        .join(MediaAsso, Media.id == MediaAsso.media_id)
        .filter(
            MediaAsso.entity_type == entity_type,
            MediaAsso.entity_id == entity_id
        )
        .all()
    )


def get_portrait_by_entity(
    db : Session,
    entity_type : str,
    entity_id : int,
    media_role : str
):
    result = db.query(Media).join(MediaAsso, Media.id == MediaAsso.media_id).filter(
        MediaAsso.entity_type == entity_type,
        MediaAsso.entity_id == entity_id,
        MediaAsso.role == media_role
    ).first()

    return result
    

