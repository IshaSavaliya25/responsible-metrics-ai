import json

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.paper import Paper


router = APIRouter(

    prefix="/api/history",

    tags=["Analysis History"]

)


# =========================================================
# SAFE JSON LOAD
# =========================================================

def safe_json_loads(value):

    if not value:

        return {}

    if isinstance(value, dict):

        return value

    if isinstance(value, list):

        return value

    try:

        return json.loads(value)

    except Exception:

        return {}


# =========================================================
# GET ALL PAPER ANALYSES
# =========================================================

@router.get("/")
def get_analysis_history(

    db: Session = Depends(get_db)

):

    papers = (

        db.query(Paper)

        .order_by(
            Paper.created_at.desc()
        )

        .all()

    )


    return {

        "total":

            len(papers),


        "papers": [

            {

                "id":
                    paper.id,


                "filename":
                    paper.filename,


                "title":
                    paper.title,


                "page_count":
                    paper.page_count,


                "word_count":
                    paper.word_count,


                "responsible_score":
                    paper.responsible_score,


                "responsible_rating":
                    paper.responsible_rating,


                "compliance_score":
                    paper.compliance_score,


                "novelty_level":
                    paper.novelty_level,


                "average_similarity":
                    paper.average_similarity,


                "created_at":

                    paper.created_at.isoformat()
                    if paper.created_at
                    else None

            }

            for paper in papers

        ]

    }


# =========================================================
# GET SINGLE PAPER ANALYSIS
# =========================================================

@router.get("/{paper_id}")
def get_paper_analysis(

    paper_id: int,

    db: Session = Depends(get_db)

):

    paper = (

        db.query(Paper)

        .filter(
            Paper.id == paper_id
        )

        .first()

    )


    if not paper:

        raise HTTPException(

            status_code=404,

            detail="Paper analysis not found."

        )


    # Parse JSON fields

    nlp_analysis = safe_json_loads(
        paper.nlp_analysis
    )


    bibliometric_analysis = safe_json_loads(
        paper.bibliometric_analysis
    )


    responsible_metrics_analysis = safe_json_loads(
        paper.responsible_metrics_analysis
    )


    principle_analysis = safe_json_loads(
        paper.principle_analysis
    )


    research_gap_analysis = safe_json_loads(
        paper.research_gap_analysis
    )


    multi_level_analysis = safe_json_loads(
        paper.multi_level_analysis
    )

    if not multi_level_analysis or multi_level_analysis.get("overall_score") == 0:
        import os
        from app.config import settings
        from app.services.pdf_service import PDFService
        from app.services.multi_level_framework_service import MultiLevelFrameworkService

        ml_service = MultiLevelFrameworkService()
        recomputed = None

        if paper.file_id and os.path.exists(settings.UPLOAD_DIR):
            matching_files = [f for f in os.listdir(settings.UPLOAD_DIR) if f.startswith(str(paper.file_id))]
            if matching_files:
                pdf_path = os.path.join(settings.UPLOAD_DIR, matching_files[0])
                try:
                    pdf_data = PDFService.extract_text(pdf_path)
                    if isinstance(pdf_data, dict) and pdf_data.get("text"):
                        recomputed = ml_service.analyze(pdf_data["text"])
                except Exception:
                    pass

        if not recomputed or recomputed.get("overall_score", 0) == 0:
            fallback_text = f"{paper.title or ''} {paper.filename or ''} "
            if isinstance(nlp_analysis, dict):
                for k in ["research_problem", "methodology", "contributions", "key_findings"]:
                    v = nlp_analysis.get(k)
                    if isinstance(v, list):
                        fallback_text += " ".join([str(x) for x in v]) + " "
                    elif isinstance(v, str):
                        fallback_text += v + " "
            if fallback_text.strip():
                recomputed = ml_service.analyze(fallback_text)

        if recomputed and recomputed.get("overall_score", 0) > 0:
            multi_level_analysis = recomputed
            try:
                paper.multi_level_analysis = json.dumps(recomputed)
                db.commit()
            except Exception:
                pass


    return {

        # =====================================================
        # BASIC INFORMATION
        # =====================================================

        "id":

            paper.id,


        "filename":

            paper.filename,


        "title":

            paper.title,


        "created_at":

            paper.created_at.isoformat()
            if paper.created_at
            else None,


        # =====================================================
        # PAPER INFORMATION
        # =====================================================

        "paper_information": {

            "page_count":

                paper.page_count
                if paper.page_count is not None
                else 0,


            "word_count":

                paper.word_count
                if paper.word_count is not None
                else 0,


            "character_count":

                paper.character_count
                if paper.character_count is not None
                else 0

        },


        # =====================================================
        # SCORES
        # =====================================================

        "responsible_metrics": {

            "score":

                paper.responsible_score
                if paper.responsible_score is not None
                else 0,


            "rating":

                paper.responsible_rating
                or "Not Available"

        },


        "principle_summary": {

            "compliance_score":

                paper.compliance_score
                if paper.compliance_score is not None
                else 0

        },


        "research_gap_summary": {

            "novelty_level":

                paper.novelty_level
                or "Unknown",


            "average_similarity":

                paper.average_similarity
                if paper.average_similarity is not None
                else 0

        },


        # =====================================================
        # COMPLETE ANALYSIS
        # =====================================================

        "nlp_analysis":

            nlp_analysis,


        "bibliometric_analysis":

            bibliometric_analysis,


        "responsible_metrics_analysis":

            responsible_metrics_analysis,


        "principle_analysis":

            principle_analysis,


        "research_gap_analysis":

            research_gap_analysis,


        "multi_level_analysis":

            multi_level_analysis

    }


# =========================================================
# DELETE PAPER
# =========================================================

@router.delete("/{paper_id}")
def delete_paper_analysis(

    paper_id: int,

    db: Session = Depends(get_db)

):

    paper = (

        db.query(Paper)

        .filter(
            Paper.id == paper_id
        )

        .first()

    )


    if not paper:

        raise HTTPException(

            status_code=404,

            detail="Paper analysis not found."

        )


    db.delete(
        paper
    )


    db.commit()


    return {

        "message":

            "Paper analysis deleted successfully"

    }