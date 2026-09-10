from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from crud.medias import (
    save_media_file,
    create_media,
    create_media_association,
    get_media_by_entity
)
from schemas.mediaAssoCreation import MediaAssoCreation
from schemas.mediaEntitySortie import MediaForEntitySortie


router = APIRouter(
    prefix="/media",
    tags=["Media"]
)

@router.post("/upload")
async def upload_media(
    file: UploadFile = File(...),
    type: str = Form(...),
    db: Session = Depends(get_db)
):
    media_data = save_media_file(file, type)

    media = create_media(db, media_data)

    return media


@router.post("/{media_id}/associate")
def associate_media(
    media_id: int,
    association: MediaAssoCreation,
    db: Session = Depends(get_db)
):
    return create_media_association(
        db,
        media_id,
        association
    )


@router.get("/{entity_type}/{entity_id}", response_model=list[MediaForEntitySortie])
def get_media_for_entity(
    entity_type: str,
    entity_id: int,
    db: Session = Depends(get_db)
):
    results = get_media_by_entity(
        db,
        entity_type,
        entity_id
    )

    return [
        {
            **media.__dict__,
            "role": role,
            "url": f"/media-files/{media.chemin}"
        }
        for media, role in results
    ]
