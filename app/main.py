# from dotenv import load_dotenv
# load_dotenv()
# from fastapi import FastAPI
# from .database import Base, engine
# from .routes import auth, employees


# Base.metadata.create_all(bind=engine)



# app = FastAPI(title="Crewzy Employee Directory")

# app.include_router(auth.router)
# app.include_router(employees.router)

# @app.get("/")
# def root():
#     return {"message": "Backend is running"}



from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import auth, employees
from .database import Base, engine

app = FastAPI(title="Crewzy Employee Directory")

# ✅ CORS MUST COME FIRST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # TEMPORARY: allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# THEN DB
Base.metadata.create_all(bind=engine)

# THEN ROUTES
app.include_router(auth.router)
app.include_router(employees.router)

@app.get("/")
def root():
    return {"message": "Backend is running"}
