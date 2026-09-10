from pathlib import Path
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from db.database import get_db
from crud.articles import create_article, get_all_articles, get_article, update_article, delete_article, get_last_article
from crud.cheikhs import get_all_cheikhs, get_cheikh, get_last_cheikh, create_cheikh, update_cheikh, delete_cheikh
from crud.medias import (
    get_media_by_entity,
    get_portrait_by_entity
)

from schemas.articleCreation import ArticleCreation
from schemas.articleMaj import ArticleMaj
from schemas.cheikhCreation import CheikhCreation
from schemas.cheikhMaj import CheikhMaj

from routers.media import router as media_router
from models.medias import Media
from models.media_asso import MediaAsso

app = FastAPI(title="Blog WFuta")

origins = [
    "http://127.0.0.1:5501"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(media_router)


BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR / "storage" / "media"

app.mount(
    "/media-files",
    StaticFiles(directory=MEDIA_DIR),
    name="media-files"
)
app.mount(
    "/styles", 
    StaticFiles(directory=BASE_DIR / "templates/styles"), 
    name="styles"
)
app.mount(
    "/assets", 
    StaticFiles(directory=BASE_DIR / "templates/assets"), 
    name="assets"
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/")
def home(request : Request, db : Session = Depends(get_db)):
    try:
        db_article = get_last_article(db)
        articles = get_all_articles(db)
        cheikhs = get_last_cheikh(db)
        context = {
            "lastArticle": db_article,
            "articles" : articles,
            "cheikhs" : cheikhs,
            "active_page" : "home"
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur interne")
    
    return templates.TemplateResponse(
        request=request, name="home.html", context=context
    )


@app.get("/blog")
async def getArticles(request : Request, db : Session = Depends(get_db)):
    try:
        db_articles = get_all_articles(db)
        context = {
            "articles": db_articles,
            "active_page" : "blog"
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur interne")
    
    return templates.TemplateResponse(
        request=request, name="blog.html", context=context
    )


#Get single Article from db
@app.get("/articles/{article_id}")
def getArticle(article_id : int, db : Session = Depends(get_db)):
    try:
        db_article = get_article(article_id, db)        
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur interne")
    return db_article


#Show signle article detail
@app.get("/singlePost/{article_id}")
def single_post(request: Request, article_id: int, db: Session = Depends(get_db)):

    db_article = get_article(article_id, db)

    results = get_media_by_entity(
        db,
        "article",
        article_id
    )

    medias = [
        {
            "id": media.id,
            "nom": media.nom,
            "chemin": media.chemin,
            "type": media.type,
            "mime_type": media.mime_type,
            "taille": media.taille,
            "role": role,
            "url": f"/media-files/{media.chemin}"
        }

        for media, role in results
    ]
    
    
    if not any(role == "cover" for media, role in results):
        medias.append({
            "id": None,
            "nom": "Default Cover",
            "chemin": None,
            "type": "image",
            "mime_type": "image/jpeg",
            "taille": "",
            "role": "cover",
            "url": "/media-files/photos/default-blog.jpg"
        })

    latests_articles = get_last_article(db)

    context = {
        "article": db_article,
        "medias" : medias,
        "latests" : latests_articles,
        "active_page" : "blog"
    }


    return templates.TemplateResponse(
        request=request,
        name="singlePost.html",
        context=context
    )


@app.post("/articles")
def createArticle(a : ArticleCreation, db : Session = Depends(get_db)):
    try:
        db_article = create_article(a, db)
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur interne")
    return db_article


@app.put("/articles/{article_id}")
def updateArticle(artticle_id : int, article : ArticleMaj, db : Session = Depends(get_db)):
    try:
        db_article = update_article(artticle_id, article, db)
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur interne")
    if not db_article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return db_article


@app.delete("/articles/{article_id}")
def deleteArticle(article_id : int, db : Session = Depends(get_db)):
    try:
        db_article = delete_article(article_id, db)
        if not db_article:
            raise HTTPException(status_code=404, detail="Article non trouvé")
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur interne")
    return {"message" : "Article supprimé avec succès!", "id" : article_id}



#Cheikhs routes
@app.get("/cheikhs")
def getCheikhs(request: Request, db : Session = Depends(get_db)):
    try:
        db_cheikhs = get_all_cheikhs(db)

        context = {
            "cheikhs" : db_cheikhs,
            "active_page" : "cheikhs",
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur interne")

    return templates.TemplateResponse(
        request=request,
        name="cheikhs.html",
        context=context
    )


@app.get("/cheikhs/{id_cheikh}")
def getCheikh(request: Request, id_cheikh : int, db : Session = Depends(get_db)):
    try:
        db_cheikh = get_cheikh(id_cheikh, db)

        results = get_media_by_entity(
            db,
            "cheikh",
            id_cheikh
        )

        medias = [
            {
                "id": media.id,
                "nom": media.nom,
                "chemin": media.chemin,
                "type": media.type,
                "mime_type": media.mime_type,
                "taille": media.taille,
                "role": role,
                "url": f"/media-files/{media.chemin}" if media.chemin else "/media-files/photos/default-portrait.jpg"
            }

            for media, role in results
        ]


        if not any(role == "portrait" for media, role in results):
            medias.append({
                "id": None,
                "nom": "Portrait par défaut",
                "chemin": None,
                "type": "image",
                "mime_type": "image/jpeg",
                "taille": "",
                "role": "portrait",
                "url": "/media-files/photos/default-portrait.jpg"
            })

        context = {
            "cheikh" : db_cheikh,
            "medias" : medias,
            "active_page" : "cheikhs"
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur interne")

    return templates.TemplateResponse(
        request=request,
        name="singleCheikh.html",
        context=context
    )


@app.post("/cheikhs")
def createCheikh(a : CheikhCreation, db : Session = Depends(get_db)):
    try:
        db_cheikh = create_cheikh(a, db)
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur interne")
    return db_cheikh


@app.get("/actu")
def getActu(request: Request, db : Session = Depends(get_db)):
    context = {
        "active_page" : "actu"
    }
    return templates.TemplateResponse(
        request=request,
        name="news.html",
        context=context
    )


@app.get("/stories")
def getStories(request: Request, db : Session = Depends(get_db)):
    context = {
        "active_page" : "stories"
    }
    return templates.TemplateResponse(
        request=request,
        name="stories.html",
        context=context
    )
