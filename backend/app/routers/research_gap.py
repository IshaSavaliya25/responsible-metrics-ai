from fastapi import APIRouter

from app.services.research_gap_service import (
    ResearchGapService
)


router = APIRouter(

    prefix="/api/research-gap",

    tags=["Research Gap Detection"]
)


@router.post("/detect")
async def detect_research_gap(
    data: dict
):

    title = data.get(
        "title",
        ""
    )

    abstract = data.get(
        "abstract",
        ""
    )

    keywords = data.get(
        "keywords",
        []
    )


    query_paper = {

        "title": title,

        "abstract": abstract,

        "keywords": keywords
    }


    service = ResearchGapService()


    result = service.detect_gap(
        query_paper
    )


    return {

        "message":
            "Potential research gap analysis completed",

        "result":
            result
    }