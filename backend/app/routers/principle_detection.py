from fastapi import APIRouter

from app.services.principle_detection_service import (
    PrincipleDetectionService
)


router = APIRouter(

    prefix="/api/principles",

    tags=["Principle Detection"]
)


@router.post("/analyze")
async def analyze_principles(
    data: dict
):

    text = data.get(
        "text",
        ""
    )


    if not text:

        return {

            "message":
                "No text provided.",

            "analysis":
                {}
        }


    service = (
        PrincipleDetectionService()
    )


    result = service.analyze(
        text
    )


    return {

        "message":
            "Responsible principles analysis completed successfully",

        "analysis":
            result
    }   