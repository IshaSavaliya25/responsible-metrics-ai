from fastapi import APIRouter

from app.services.responsible_metrics_service import (
    ResponsibleMetricsService
)


router = APIRouter(

    prefix="/api/responsible-metrics",

    tags=["Responsible Metrics"]
)


@router.post("/evaluate")
async def evaluate_responsible_metrics(
    data: dict
):

    bibliometric_data = data.get(
        "bibliometric_data",
        {}
    )

    nlp_analysis = data.get(
        "nlp_analysis",
        {}
    )

    sections = data.get(
        "sections",
        {}
    )


    service = ResponsibleMetricsService()


    result = service.evaluate(

        bibliometric_data,

        nlp_analysis,

        sections
    )


    return {

        "message":
            "Responsible metrics evaluation completed successfully",

        "result":
            result
    }