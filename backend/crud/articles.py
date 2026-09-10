from sqlalchemy.exc import SQLAlchemyError
from schemas.articleCreation import ArticleCreation
from schemas.articleMaj import ArticleMaj
from sqlalchemy.orm import Session
from models.articles import Article

from .medias import get_portrait_by_entity

def create_article(a : ArticleCreation, db : Session):
    try:
        db_article = Article(
            titre = a.titre,
            excert = a.excert,
            content = a.content,
            dateCreation = a.dateCreation,
            dateMaj = a.dateMaj
        )

        db.add(db_article)
        db.commit()
        db.refresh(db_article)

        return db_article
    except SQLAlchemyError as e:
        db.rollback()
        raise


def update_article(id : int, a : ArticleMaj, db : Session):
    try:
        #Get the article from the database
        db_article = db.query(Article).filter(Article.id == id).first()
        if not db_article:
            return None

        #Fill in the columns with the values
        for cle, valeur in a.dict(exclude_unset=True).items():
            setattr(db_article, cle, valeur)

        db.commit()
        db.refresh(db_article)

        return db_article
    except SQLAlchemyError as e:
        db.rollback()
        raise


def get_all_articles(db : Session):
    try:
        db_articles = db.query(Article).all()

        for article in db_articles:
            result = get_portrait_by_entity(db, "article", article.id, "cover")
            if not result :
                article.cover = "/media-files/photos/default-blog.jpg"
            else : 
                article.cover =  f"/media-files/{result.chemin}"

        return db_articles
    
    except SQLAlchemyError:
        raise


def get_last_article(db : Session):
    try:
        db_article = db.query(Article).order_by(
            Article.dateCreation.desc(),
            Article.id.desc()
        ).limit(4).all()

        for article in db_article:
            result = get_portrait_by_entity(db, "article", article.id, "cover")
            if not result :
                article.cover = "/media-files/photos/default-blog.jpg"
            else : 
                article.cover =  f"/media-files/{result.chemin}"

        return db_article
    except SQLAlchemyError:
        raise


def get_article(id : int, db : Session):
    try:
        db_article = db.query(Article).filter(Article.id == id).first()
        return db_article
    except SQLAlchemyError:
        raise


def delete_article(id : int, db : Session):
    try:
        db_article = db.query(Article).filter(Article.id == id).first()

        if not db_article:
            return None

        db.delete(db_article)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise    
    