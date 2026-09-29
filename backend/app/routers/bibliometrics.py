from fastapi import APIRouter, HTTPException

from app.services.openalex_service import (
    OpenAlexService
)


router = APIRouter(
    prefix="/api/bibliometrics",
    tags=["Bibliometrics"]
)


@router.get("/search")
async def search_paper(title: str):

    try:

        work = await OpenAlexService.search_paper_by_title(
            title
        )

        if not work:

            raise HTTPException(
                status_code=404,
                detail="Paper not found in OpenAlex."
            )

        bibliometric_data = (
            OpenAlexService.extract_bibliometric_data(
                work
            )
        )

        return {
            "message": "Bibliometric data retrieved successfully",
            "data": bibliometric_data
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )