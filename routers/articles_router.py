from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_cursor
from schemas import schemas_dto
from models.Article import Article
from models.User import User
import utilities

from pydantic.typing import Annotated
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

router = APIRouter(
    prefix='/articles',
    tags=['Articles']
)

#Get all articles
@router.get("")
async def get_articles(
    cursor: Session= Depends(get_cursor),
    limit: int=10, 
    offset: int=0
    ):
    all_articles = cursor.query(Article).limit(limit).offset(offset).all() # Get limit Article 
    article_count= cursor.query(func.count(Article.id)).scalar() #Count total article in DB
    return {
        "articles": all_articles,
        "limit": limit,
        "total": article_count,
        "skip": offset
    } 
#Get articles by Id
@router.get("/{article_id}")
async def get_article_by_id(article_id: int, response: Response, cursor: Session= Depends(get_cursor)):
    # corresponding_article = {}
    # id = get_corresponding_article(article_id)

    corresponding_article = cursor.query(Article).filter_by(id = article_id).first() # Filter Article 
    if not corresponding_article: # Raise error if there is not article
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "Article not found"
        )
    return corresponding_article


#Post Article

@router.post("", status_code= status.HTTP_201_CREATED)
async def create_articles(
    payload: schemas_dto.Article_POST_UPDATE_Body,
    token: Annotated[str, Depends(oauth2_scheme)],
    cursor:Session= Depends(get_cursor)
    ):
    # Le décodage du token permet de récupérer l'identifiant du user
    decoded_user_id = utilities.decode_token(token)
    corresponding_user = cursor.query(User).filter(User.id == decoded_user_id).first()
    # print(corresponding_user)
    new_article = Article(
        title = payload.title,
        content = payload.content,
        img = payload.img,
        user_id = corresponding_user.id
    ) # build the insert
    cursor.add(new_article) # Send the query
    cursor.commit() #Save the staged change
    cursor.refresh(new_article)
    return {"message": "Bingo new article {brand} added successfully with id: {id} ".format(brand = new_article.title, id= new_article.id)}


#Delete article

@router.delete('/{article_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id:int,
    token: Annotated[str, Depends(oauth2_scheme)],
    cursor:Session=Depends(get_cursor)
    ):
    
    decoded_user_id = utilities.decode_token(token)
    corresponding_user = cursor.query(User).filter(User.id == decoded_user_id).first()
    # print(corresponding_user)
        
    
    corresponding_article = cursor.query(Article).filter_by(id = article_id)
    if corresponding_article.first():
        # Continue to delete
        corresponding_article.delete() # supprime
        cursor.commit() # commit the stated changes (changement latent)
        return 
    else:
        raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        detail= "Article not found with id: {id} ".format(id= article_id)
    ) 


# Update
@router.patch('/{article_id}')
async def update_article(
    article_id: int,
    token: Annotated[str, Depends(oauth2_scheme)],
    payload:schemas_dto.Article_POST_UPDATE_Body, 
    cursor:Session=Depends(get_cursor)
    ):
    decoded_user_id = utilities.decode_token(token)
    user_auth = cursor.query(User).filter(User.id == decoded_user_id).first()

    # Recherce si la article existe  
    corresponding_article = cursor.query(Article).filter_by(id = article_id)
    if corresponding_article.first():
        # mise à jour (quoi avec quelle valeur ?) Body -> DTO
        corresponding_article.update({
            "price": payload.price,
            "description": payload.description,
            "availability": payload.availability,
            "rating": payload.rating
        })
        cursor.commit() #Save modification
        return corresponding_article.first()
    else: 
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding product with id: {article_id}'
        )