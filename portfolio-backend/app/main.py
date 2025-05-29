from fastapi import FastAPI
from app.database import Base, engine
from app.auth.routes import router as auth_router
from app.users.routes import router as user_router
from app import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
#Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "Welcome to Portfolio API"}
