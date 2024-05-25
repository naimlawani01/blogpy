from fastapi import FastAPI
from models import User, Article
from app.database import database_engine
from fastapi.middleware.cors import CORSMiddleware

#Import des routers
import routers.articles_router, routers.users_router, routers.auth_router

# Créer les tables si elles ne sont pas présente dans la DB
User.Base.metadata.create_all(bind=database_engine)
Article.Base.metadata.create_all(bind=database_engine)



#Lancement de l'API
app= FastAPI( 
    title="Blogy")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
# Ajouter les routers dédiés
app.include_router(routers.auth_router.router)
app.include_router(routers.users_router.router)
app.include_router(routers.articles_router.router)