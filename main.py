from fastapi import FastAPI
from models import User, Article
from app.database import database_engine


#Import des routers
import routers.articles_router, routers.users_router, routers.auth_router

# Créer les tables si elles ne sont pas présente dans la DB
User.Base.metadata.create_all(bind=database_engine)
Article.Base.metadata.create_all(bind=database_engine)



#Lancement de l'API
app= FastAPI( 
    title="Blogy")

# Ajouter les routers dédiés
app.include_router(routers.auth_router.router)
app.include_router(routers.users_router.router)
app.include_router(routers.articles_router.router)