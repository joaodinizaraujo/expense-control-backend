from fastapi import FastAPI

from src.routes import user

# base.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FAAAALA ALEX", description="quero me mata")

app.include_router(user.router)


@app.get("/")
def keep_alive():
    return {"message": "bom dia."}
