from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import upload, chat
from app.core.llm import init_llm


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_llm()
    yield


app = FastAPI(title="CSV/XLSX LangChain Agent API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST","GET"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(chat.router)


@app.get("/")
async def health_check():
    return {"status": "healthy"}
