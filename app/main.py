from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from .database import Base, engine
from .routes import auth, employees


Base.metadata.create_all(bind=engine)



app = FastAPI(title="Crewzy Employee Directory")

app.include_router(auth.router)
app.include_router(employees.router)

@app.get("/")
def root():
    return {"message": "Backend is running"}
