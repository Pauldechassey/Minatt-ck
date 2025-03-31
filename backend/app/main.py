from fastapi import FastAPI

from app.routes import user, audit, domaine, attaque, sous_domaine

app = FastAPI()

app.include_router(user.router)
app.include_router(audit.router)
app.include_router(domaine.router)
app.include_router(attaque.router)
app.include_router(sous_domaine.router)

@app.get("/")
def root():
    return {"message": "Hello World"}