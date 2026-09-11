from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from crud.articles import get_all_articles, get_article, get_last_article
from crud.cheikhs import get_all_cheikhs, get_cheikh, get_last_cheikh
from crud.medias import get_media_by_entity
from db.database import get_db


BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
router = APIRouter(tags=["Pages web"])


def build_media_context(
    db: Session,
    entity_type: str,
    entity_id: int,
    default_role: str,
    default_url: str,
):
    results = get_media_by_entity(db, entity_type, entity_id)
    medias = [
        {
            "id": media.id,
            "nom": media.nom,
            "chemin": media.chemin,
            "type": media.type,
            "mime_type": media.mime_type,
            "taille": media.taille,
            "role": role,
            "url": f"/media-files/{media.chemin}",
        }
        for media, role in results
    ]

    if not any(role == default_role for _, role in results):
        medias.append(
            {
                "id": None,
                "nom": "Média par défaut",
                "chemin": None,
                "type": "image",
                "mime_type": "image/jpeg",
                "taille": 0,
                "role": default_role,
                "url": default_url,
            }
        )
    return medias


@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    try:
        context = {
            "lastArticle": get_last_article(db),
            "articles": get_all_articles(db),
            "cheikhs": get_last_cheikh(db),
            "active_page": "home",
        }
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur interne") from error
    return templates.TemplateResponse(request=request, name="home.html", context=context)


@router.get("/blog")
def blog(request: Request, db: Session = Depends(get_db)):
    try:
        context = {"articles": get_all_articles(db), "active_page": "blog"}
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur interne") from error
    return templates.TemplateResponse(request=request, name="blog.html", context=context)


@router.get("/singlePost/{article_id}")
def single_post(request: Request, article_id: int, db: Session = Depends(get_db)):
    try:
        article = get_article(article_id, db)
        if article is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article non trouvé")
        context = {
            "article": article,
            "medias": build_media_context(db, "article", article_id, "cover", "/media-files/photos/default-blog.jpg"),
            "latests": get_last_article(db),
            "active_page": "blog",
        }
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur interne") from error
    return templates.TemplateResponse(request=request, name="singlePost.html", context=context)


@router.get("/cheikhs")
def cheikhs(request: Request, db: Session = Depends(get_db)):
    try:
        context = {"cheikhs": get_all_cheikhs(db), "active_page": "cheikhs"}
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur interne") from error
    return templates.TemplateResponse(request=request, name="cheikhs.html", context=context)


@router.get("/cheikhs/{cheikh_id}")
def single_cheikh(request: Request, cheikh_id: int, db: Session = Depends(get_db)):
    try:
        cheikh = get_cheikh(cheikh_id, db)
        if cheikh is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cheikh non trouvé")
        context = {
            "cheikh": cheikh,
            "medias": build_media_context(db, "cheikh", cheikh_id, "portrait", "/media-files/photos/default-portrait.jpg"),
            "active_page": "cheikhs",
        }
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur interne") from error
    return templates.TemplateResponse(request=request, name="singleCheikh.html", context=context)


@router.get("/actu")
def news(request: Request):
    return templates.TemplateResponse(request=request, name="news.html", context={"active_page": "actu"})


@router.get("/stories")
def stories(request: Request):
    return templates.TemplateResponse(request=request, name="stories.html", context={"active_page": "stories"})
