from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import database
from schemas import schemas_dto
from models.User import User
import utilities
from typing import List

from pydantic.typing import Annotated
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


#Create custumer
@router.post('', response_model=schemas_dto.User_response, status_code= status.HTTP_201_CREATED)
async def create_user(
    payload: schemas_dto.User_POST_Body, 
    cursor: Session = Depends(database.get_cursor),
    ):
    try: 
        hashed_password = utilities.hash_password(payload.password)
        new_user= User(password=hashed_password, username= payload.username, nom= payload.nom)
        cursor.add(new_user) # Send query
        cursor.commit() # Save the staged changes
        cursor.refresh(new_user) # Pour obtenir l'identifiant
        # return {'message':f'The user has been created with the id: {new_user.id}'}
        return new_user # not a python dict -> donc il faut un mapping
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists" 
        )
#Get all custumer
@router.get('', response_model=List[schemas_dto.User_response])
async def get_all_users(
    token: Annotated[str, Depends(oauth2_scheme)],
    cursor: Session = Depends(database.get_cursor)
    ):
    all_users = cursor.query(User).all()  #Query Get all user
    return all_users
#Get custumer by ID
@router.get('/{user_id}', response_model=schemas_dto.User_response)
async def get_user_by_id(user_id:int, cursor: Session = Depends(database.get_cursor)):
    corresponding_user = cursor.query(User).filter(User.id == user_id).first() # Recher du user correspondant
    if(corresponding_user): # Check si le user exist
        return corresponding_user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No user with id:{user_id}'
        )
#Udpate custumer

@router.patch('/{user_id}')
async def update_user(
    user_id: int, 
    payload:schemas_dto.User_UPDATE_Body,
    token: Annotated[str, Depends(oauth2_scheme)],
    cursor:Session=Depends(database.get_cursor)
    ):

    corresponding_user = cursor.query(User).filter_by(id = user_id)
    if corresponding_user.first():
        # mise à jour (quoi avec quelle valeur ?) Body -> DTO
        corresponding_user.update({
            "nom": payload.nom,
            "username": payload.username
        })
        cursor.commit()
        return corresponding_user.first()
    else: 
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Ne corresponding product with id: {user_id}'
        )

   