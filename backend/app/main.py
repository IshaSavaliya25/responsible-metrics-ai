import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import (
    Base,
    engine
)
from app.models.paper import Paper
from app.routers import (
    paper_analysis,
    history,
    upload,
    analysis,
    bibliometrics,
    principle_detection,
    research_gap,
    responsible_metrics
)

logger = logging.getLogger("uvicorn.info")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup pre-warming and shutdown cleanup.
    """
    logger.info("Initializing ResponsibleMetrics AI database schema...")
    Base.metadata.create_all(bind=engine)

    logger.info("Pre-warming SBERT SentenceTransformer embeddings service...")
    try:
        from app.ml.embeddings import EmbeddingService
        embedding_service = EmbeddingService()
        embedding_service.encode("Pre-warming SBERT embedding model for scientific evaluation.")
        logger.info("SentenceTransformer model successfully loaded and pre-warmed.")
    except Exception as exc:
        logger.warning(f"Embedding pre-warming completed with notice: {exc}")

    yield

    logger.info("ResponsibleMetrics AI Backend shutting down gracefully.")


app = FastAPI(
    title="ResponsibleMetrics AI",
    description=(
        "An NLP-Based Multi-Level Framework for "
        "Responsible Use of Bibliometric Indicators"
    ),
    version="1.0.0",
    lifespan=lifespan
)

# Enable Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core Paper Analysis Pipeline & History
app.include_router(paper_analysis.router)
app.include_router(history.router)

# Modular Microservice Routers
app.include_router(upload.router)
app.include_router(analysis.router)
app.include_router(bibliometrics.router)
app.include_router(principle_detection.router)
app.include_router(research_gap.router)
app.include_router(responsible_metrics.router)


@app.get("/")
def root():
    return {
        "message": "ResponsibleMetrics AI Backend is Running",
        "version": "1.0.0",
        "docs_url": "/docs"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ResponsibleMetrics AI"
    }