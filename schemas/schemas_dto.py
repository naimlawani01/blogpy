from datetime import datetime
from pydantic import BaseModel, Field
# DTO : Data Transfert Object



class Article_POST_UPDATE_Body (BaseModel):
    title : str
    content : str
    img: str




class Article_response (BaseModel):
    id: int
    title : str
    content : str
    img: str
    user_id: int
    class Config: # Importante pour la traduction ORM->DTO
        orm_mode= True

class User_response (BaseModel):
    id: int
    nom: str
    username:str
    class Config: # Importante pour la traduction ORM->DTO
        orm_mode= True


class User_POST_Body (BaseModel):
    username:str
    nom: str
    password: str

class User_UPDATE_Body (BaseModel):
    username:str
    nom: str
    password: str

