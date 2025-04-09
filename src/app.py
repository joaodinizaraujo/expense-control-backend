from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import (
    users,
    transactions,
    transaction_types,
    currencies,
    transaction_categories
)

# base.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="expense-control",
    description="expense-control service",
    root_path="/api/v1"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://gerenciador-despesas-three.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(transaction_types.router)
app.include_router(currencies.router)
app.include_router(transaction_categories.router)


@app.get("/")
def keep_alive():
    return {"message": "calabreso"}
