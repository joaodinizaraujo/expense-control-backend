from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import user

# base.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FAAAALA ALEX",
    description="quero me mata",
    root_path="/api/v1"
)

app.include_router(user.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def keep_alive():
    return {"message": "calabreso"}
