from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers.articles import router as articles_router
from routers.cheikhs import router as cheikhs_router
from routers.media import router as media_router
from routers.web import router as web_router


BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR / "storage" / "media"

app = FastAPI(title="Blog WFuta")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media-files", StaticFiles(directory=MEDIA_DIR), name="media-files")
app.mount(
    "/styles",
    StaticFiles(directory=BASE_DIR / "templates" / "styles"),
    name="styles",
)
app.mount(
    "/assets",
    StaticFiles(directory=BASE_DIR / "templates" / "assets"),
    name="assets",
)

app.include_router(web_router)
app.include_router(articles_router)
app.include_router(cheikhs_router)
app.include_router(media_router)
