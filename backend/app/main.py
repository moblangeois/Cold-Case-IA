from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.api import chat, cases, files
from app.services.embeddings import EmbeddingsService

load_dotenv()

# Initialize embeddings service on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    embeddings_service = EmbeddingsService()
    app.state.embeddings_service = embeddings_service
    await embeddings_service.initialize()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Cold Case IA API",
    description="API pour l'analyse de cold cases assistée par IA avec Claude Sonnet 4.5",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://coldcase.citadelle.work",
        "http://coldcase.citadelle.work"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for case data
if os.path.exists("../Kyron_Horman"):
    app.mount("/static", StaticFiles(directory="../Kyron_Horman"), name="static")

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(cases.router, prefix="/api/cases", tags=["cases"])
app.include_router(files.router, prefix="/api/files", tags=["files"])

@app.get("/")
async def root():
    return {
        "message": "Cold Case IA API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
