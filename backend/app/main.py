from fastapi import FastAPI
from .routes import user, audit, domaine, attaque, sous_domaine

app = FastAPI()

app.include_router(user.router)
app.include_router(audit.router)
app.include_router(domaine.router)
app.include_router(attaque.router)
app.include_router(sous_domaine.router)

@app.get("/")
def root():
    return {"message": "Hello World"}

import logging

logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG for more verbose output
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# uvicorn backend.app.main:app --reload    -> to run the backend
# python3 attaque/test_state/test_vuln.py  -> to run the website_test
