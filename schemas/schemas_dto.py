from datetime import datetime
from pydantic import BaseModel, Field
# DTO : Data Transfert Object



class Article_POST_UPDATE_Body (BaseModel):
    title : str
    content : str




class Article_response (BaseModel):
    id: int
    email:str
    role: str
    create_at: datetime
    class Config: # Importante pour la traduction ORM->DTO
        orm_mode= True

class User_response (BaseModel):
    id: int
    nom: str
    email:str
    class Config: # Importante pour la traduction ORM->DTO
        orm_mode= True


class User_POST_Body (BaseModel):
    email:str
    nom: str
    password: str

class User_UPDATE_Body (BaseModel):
    email:str
    nom: str
    password: str

