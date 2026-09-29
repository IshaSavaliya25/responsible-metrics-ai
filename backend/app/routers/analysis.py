from fastapi import APIRouter

from app.services.nlp_service import NLPService


router = APIRouter(
    prefix="/api/analysis",
    tags=["NLP Analysis"]
)


@router.post("/analyze-text")
async def analyze_text(data: dict):

    """
    Analyze structured research paper sections.
    """

    nlp_service = NLPService()

    sections = data.get(
        "sections",
        {}
    )

    analysis = nlp_service.analyze_paper(
        sections
    )

    return {

        "message": "NLP analysis completed successfully",

        "analysis": analysis
    }