from fastapi import FastAPI
from app.database import init_db
from app.auth.routes import router as auth_router
from app.users.routes import router as user_router

app = FastAPI()

# Initialize the database (creates tables if they don't exist)
init_db()

# Include routers
app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Portfolio API"}

@app.get("/")
def root():
    return {"message": "Welcome to Portfolio API"}
