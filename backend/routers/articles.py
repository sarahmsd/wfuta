from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from crud.articles import create_article, delete_article, get_article, update_article
from db.database import get_db
from schemas.articleCreation import ArticleCreation
from schemas.articleMaj import ArticleMaj


router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("/{article_id}")
def get_article_by_id(article_id: int, db: Session = Depends(get_db)):
    try:
        article = get_article(article_id, db)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur interne") from error

    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article non trouvé")
    return article


@router.post("", status_code=status.HTTP_201_CREATED)
def create_article_endpoint(article: ArticleCreation, db: Session = Depends(get_db)):
    try:
        return create_article(article, db)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur interne") from error


@router.put("/{article_id}")
def update_article_endpoint(article_id: int, article: ArticleMaj, db: Session = Depends(get_db)):
    try:
        updated_article = update_article(article_id, article, db)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur interne") from error

    if updated_article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article non trouvé")
    return updated_article


@router.delete("/{article_id}")
def delete_article_endpoint(article_id: int, db: Session = Depends(get_db)):
    try:
        deleted = delete_article(article_id, db)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur interne") from error

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article non trouvé")
    return {"message": "Article supprimé avec succès!", "id": article_id}
