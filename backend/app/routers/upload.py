import os
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.config import settings
from app.services.pdf_service import PDFService


router = APIRouter(
    prefix="/api/upload",
    tags=["Upload"]
)


@router.post("/")
async def upload_paper(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    os.makedirs(
        settings.UPLOAD_DIR,
        exist_ok=True
    )

    file_id = str(uuid.uuid4())

    safe_filename = file.filename.replace(
        " ",
        "_"
    )

    filename = f"{file_id}_{safe_filename}"

    file_path = os.path.join(
        settings.UPLOAD_DIR,
        filename
    )

    try:

        # Save uploaded file
        with open(file_path, "wb") as buffer:

            content = await file.read()

            buffer.write(content)

        # Extract PDF content
        pdf_data = PDFService.extract_text(
            file_path
        )

        if not pdf_data["text"]:

            raise HTTPException(
                status_code=400,
                detail="No readable text found in PDF."
            )

        # Prepare section statistics
        section_statistics = {}

        for section_name, section_text in pdf_data["sections"].items():

            section_statistics[section_name] = {
                "word_count": len(section_text.split()),
                "character_count": len(section_text)
            }

        return {

            "message": "Research paper processed successfully",

            "file_id": file_id,

            "filename": file.filename,

            "statistics": {

                "page_count": pdf_data["page_count"],

                "word_count": pdf_data["word_count"],

                "character_count": pdf_data["character_count"]
            },

            "detected_sections": list(
                pdf_data["sections"].keys()
            ),

            "section_statistics": section_statistics,

            "sections_preview": {

                section_name: section_text[:500]

                for section_name, section_text
                in pdf_data["sections"].items()

                if section_text
            }
        }

    except HTTPException:

        raise

    except Exception as e:

        if os.path.exists(file_path):

            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )