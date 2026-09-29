from fastapi import FastAPI

from app.database.database import (
    Base,
    engine
)

from app.models.paper import Paper

from app.routers import paper_analysis
from app.routers import history


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="ResponsibleMetrics AI",
    description=(
        "An NLP-Based Multi-Level Framework for "
        "Responsible Use of Bibliometric Indicators"
    ),
    version="1.0.0"
)


app.include_router(
    paper_analysis.router
)

app.include_router(
    history.router
)


@app.get("/")
def root():

    return {

        "message":
            "ResponsibleMetrics AI Backend is Running"
    }


@app.get("/health")
def health_check():

    return {

        "status": "healthy"
    }