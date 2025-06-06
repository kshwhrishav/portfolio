from fastapi import FastAPI
from app.database import init_db
from app.auth.routes import router as auth_router
from app.users.routes import router as user_router
from app.projects.routes import router as project_router
from app.profile.routes import router as profile_router
from app.experience.routes import router as experience_router

app = FastAPI()

# Initialize the database (creates tables if they don't exist)
init_db()

# Include routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(project_router)
app.include_router(profile_router)
app.include_router(experience_router)

@app.get("/")
def root():
    return {"message": "Welcome to Portfolio API"}
