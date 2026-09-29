import os
import uuid
import json
import traceback
import hashlib

from typing import Any

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends
)

from sqlalchemy.orm import Session

from app.config import settings
from app.database.database import get_db
from app.models.paper import Paper

from app.services.pdf_service import PDFService
from app.services.nlp_service import NLPService
from app.services.openalex_service import OpenAlexService

from app.services.responsible_metrics_service import (
    ResponsibleMetricsService
)

from app.services.principle_detection_service import (
    PrincipleDetectionService
)

from app.services.research_gap_service import (
    ResearchGapService
)

from app.services.multi_level_framework_service import (
    MultiLevelFrameworkService
)


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/api/analyze",
    tags=["Paper Analysis"]
)


# =========================================================
# HELPER: JSON SERIALIZER
# =========================================================

def json_serializer(obj: Any):

    """
    Handles objects that are not directly
    JSON serializable.
    """

    try:

        if hasattr(obj, "item"):

            return obj.item()

    except Exception:

        pass


    if isinstance(obj, set):

        return list(obj)


    return str(obj)


# =========================================================
# HELPER: SAFE JSON CONVERSION
# =========================================================

def safe_json_dumps(data):

    """
    Convert data to JSON safely.
    """

    try:

        return json.dumps(
            data,
            default=json_serializer,
            ensure_ascii=False
        )

    except Exception as error:

        print(
            f"JSON serialization warning: {error}"
        )

        return json.dumps(
            {
                "error":
                    "Unable to serialize analysis result"
            }
        )


# =========================================================
# HELPER: SAFE FLOAT
# =========================================================

def safe_float(value):

    """
    Safely convert value to float.
    """

    if value is None:

        return None


    try:

        return float(value)

    except (
        ValueError,
        TypeError
    ):

        return None


# =========================================================
# HELPER: EXTRACT NESTED VALUE
# =========================================================

def get_nested_value(
    data,
    keys,
    default=None
):

    """
    Safely get nested dictionary value.
    """

    current = data


    for key in keys:

        if not isinstance(
            current,
            dict
        ):

            return default


        current = current.get(key)


    if current is None:

        return default


    return current


# =========================================================
# HELPER: EXTRACT RESPONSIBLE SCORE
# =========================================================

def extract_responsible_score(result):

    """
    Supports multiple possible response
    structures from ResponsibleMetricsService.
    """

    if not isinstance(result, dict):

        return None


    score = get_nested_value(
        result,
        [
            "overall",
            "responsible_metrics_score"
        ]
    )


    if score is not None:

        return safe_float(score)


    score = get_nested_value(
        result,
        [
            "overall",
            "score"
        ]
    )


    if score is not None:

        return safe_float(score)


    score = result.get(
        "responsible_metrics_score"
    )


    if score is not None:

        return safe_float(score)


    score = result.get(
        "score"
    )


    return safe_float(score)


# =========================================================
# HELPER: EXTRACT RESPONSIBLE RATING
# =========================================================

def extract_responsible_rating(result):

    """
    Extract rating safely.
    """

    if not isinstance(result, dict):

        return None


    rating = get_nested_value(
        result,
        [
            "overall",
            "rating"
        ]
    )


    if rating:

        return str(rating)


    rating = result.get(
        "rating"
    )


    if rating:

        return str(rating)


    return None


# =========================================================
# HELPER: EXTRACT PAPER TITLE
# =========================================================

def extract_paper_title(text: str):

    """
    Extract possible paper title from
    first part of PDF.
    """

    if not text:

        return None


    lines = text.split("\n")


    possible_titles = []


    ignore_words = [

        "abstract",

        "introduction",

        "keywords",

        "doi",

        "journal",

        "volume",

        "issue",

        "received",

        "accepted",

        "author",

        "authors"

    ]


    for line in lines[:40]:

        line = line.strip()


        if not line:

            continue


        if len(line) < 15:

            continue


        if line.lower() in ignore_words:

            continue


        if line.lower().startswith("doi"):

            continue


        if line.lower().startswith("http"):

            continue


        word_count = len(
            line.split()
        )


        if 4 <= word_count <= 30:

            possible_titles.append(
                line
            )


    if possible_titles:

        return possible_titles[0]


    return None


# =========================================================
# ANALYZE PAPER ENDPOINT
# =========================================================

@router.post("/paper")
async def analyze_paper(

    file: UploadFile = File(...),

    db: Session = Depends(get_db)

):


    # =====================================================
    # VALIDATE FILE
    # =====================================================

    if not file:

        raise HTTPException(

            status_code=400,

            detail="No file uploaded."

        )


    filename_check = (
        file.filename or ""
    ).lower()


    if (

        file.content_type != "application/pdf"

        and

        not filename_check.endswith(".pdf")

    ):

        raise HTTPException(

            status_code=400,

            detail="Only PDF files are allowed."

        )


    # =====================================================
    # PREPARE VARIABLES
    # =====================================================

    file_path = None


    try:


        print("\n")

        print("=" * 70)

        print("RESPONSIBLEMETRICS AI")

        print("PAPER ANALYSIS PIPELINE STARTED")

        print("=" * 70)


        # =================================================
        # STEP 1: CREATE UPLOAD DIRECTORY
        # =================================================

        print(
            "\nSTEP 1: Preparing upload directory..."
        )


        os.makedirs(

            settings.UPLOAD_DIR,

            exist_ok=True

        )


        # =================================================
        # STEP 2: GENERATE FILE ID
        # =================================================

        print(
            "STEP 2: Generating file ID..."
        )


        file_id = str(
            uuid.uuid4()
        )


        original_filename = (
            file.filename or "uploaded_paper.pdf"
        )


        safe_filename = original_filename.replace(
            " ",
            "_"
        )


        safe_filename = safe_filename.replace(
            "/",
            "_"
        )


        safe_filename = safe_filename.replace(
            "\\",
            "_"
        )


        filename = (
            f"{file_id}_{safe_filename}"
        )


        file_path = os.path.join(

            settings.UPLOAD_DIR,

            filename

        )


        # =================================================
        # STEP 3: READ AND SAVE PDF
        # =================================================

        print(
            "STEP 3: Saving uploaded PDF..."
        )


        content = await file.read()


        if not content:

            raise HTTPException(

                status_code=400,

                detail="Uploaded PDF file is empty."

            )


        # =================================================
        # GENERATE FILE HASH
        # =================================================

        file_hash = hashlib.sha256(

            content

        ).hexdigest()


        # =================================================
        # CHECK DUPLICATE PAPER
        # =================================================

        existing_paper = (

            db.query(Paper)

            .filter(
                Paper.file_hash == file_hash
            )

            .first()

        )


        if existing_paper:

            raise HTTPException(

                status_code=409,

                detail=(
                    f"This paper has already been analyzed. "
                    f"Existing Analysis ID: {existing_paper.id}"
                )

            )


        # =================================================
        # SAVE FILE
        # =================================================

        with open(

            file_path,

            "wb"

        ) as buffer:

            buffer.write(
                content
            )


        print(
            f"PDF saved successfully: {file_path}"
        )


        # =================================================
        # STEP 4: EXTRACT PDF TEXT
        # =================================================

        print(
            "\nSTEP 4: Extracting text from PDF..."
        )


        pdf_data = PDFService.extract_text(
            file_path
        )


        if not isinstance(
            pdf_data,
            dict
        ):

            raise ValueError(
                "PDFService returned invalid data format."
            )


        extracted_text = pdf_data.get(

            "text",

            ""

        )


        if not extracted_text:

            raise HTTPException(

                status_code=400,

                detail=(
                    "No readable text found in PDF. "
                    "The PDF may be scanned or image-based."
                )

            )


        print(

            f"Text extraction completed. "
            f"Characters: {len(extracted_text)}"

        )


        # =================================================
        # STEP 5: DETECT SECTIONS
        # =================================================

        print(
            "\nSTEP 5: Detecting paper sections..."
        )


        sections = pdf_data.get(

            "sections",

            {}

        )


        if not isinstance(
            sections,
            dict
        ):

            sections = {}


        print(

            "Sections detected: "
            f"{list(sections.keys())}"

        )


        # =================================================
        # STEP 6: NLP ANALYSIS
        # =================================================

        print(
            "\nSTEP 6: Starting NLP analysis..."
        )


        nlp_service = NLPService()


        nlp_analysis = nlp_service.analyze_paper(
            sections    
        )


        if nlp_analysis is None:

            nlp_analysis = {}


        print(
            "NLP analysis completed successfully."
        )


        # =================================================
        # STEP 7: EXTRACT PAPER TITLE
        # =================================================

        print(
            "\nSTEP 7: Extracting paper title..."
        )


        title = extract_paper_title(
            extracted_text
        )


        print(
            f"Detected title: {title}"
        )


        # =================================================
        # STEP 8: OPENALEX BIBLIOMETRIC SEARCH
        # =================================================

        print(
            "\nSTEP 8: Searching bibliometric data..."
        )


        bibliometric_data = {}


        if title:

            try:


                work = (

                    await OpenAlexService
                    .search_paper_by_title(
                        title
                    )

                )


                if work:


                    bibliometric_data = (

                        OpenAlexService
                        .extract_bibliometric_data(
                            work
                        )

                    )


                    if bibliometric_data is None:

                        bibliometric_data = {}


                    print(
                        "OpenAlex bibliometric data found."
                    )


                else:

                    print(
                        "No matching OpenAlex paper found."
                    )


            except Exception as openalex_error:


                print(

                    "OpenAlex warning: "
                    f"{str(openalex_error)}"

                )


                bibliometric_data = {}


        else:

            print(
                "No title detected. Skipping OpenAlex search."
            )


        # =================================================
        # STEP 9: MULTI-LEVEL FRAMEWORK ANALYSIS
        # =================================================

        print(
            "\nSTEP 9: Running Multi-Level Framework analysis..."
        )


        multi_level_framework_service = (
            MultiLevelFrameworkService()
        )


        multi_level_analysis = (

            multi_level_framework_service.analyze(
                extracted_text
            )

        )


        if multi_level_analysis is None:

            multi_level_analysis = {}


        print(
            "Multi-Level Framework analysis completed."
        )


        # =================================================
        # STEP 10: RESPONSIBLE METRICS
        # =================================================

        print(
            "\nSTEP 10: Evaluating responsible metrics..."
        )


        responsible_metrics_service = (
            ResponsibleMetricsService()
        )


        responsible_metrics_result = (

            responsible_metrics_service.evaluate(

                bibliometric_data=bibliometric_data,

                nlp_analysis=nlp_analysis,

                sections=sections

            )

        )


        if responsible_metrics_result is None:

            responsible_metrics_result = {}


        print(
            "Responsible metrics evaluation completed."
        )


        # =================================================
        # STEP 11: PRINCIPLE DETECTION
        # =================================================

        print(
            "\nSTEP 11: Detecting responsible principles..."
        )


        principle_detection_service = (
            PrincipleDetectionService()
        )


        principle_analysis = (

            principle_detection_service.analyze(
                extracted_text
            )

        )


        if principle_analysis is None:

            principle_analysis = {}


        print(
            "Principle detection completed."
        )


        # =================================================
        # STEP 12: RESEARCH GAP DETECTION
        # =================================================

        print(
            "\nSTEP 12: Detecting research gaps..."
        )


        research_gap_service = (
            ResearchGapService()
        )


        abstract = sections.get(

            "abstract",

            ""

        )


        # =================================================
        # NORMALIZE KEYWORDS
        # =================================================

        raw_keywords = nlp_analysis.get(

            "keywords",

            []

        )


        if raw_keywords is None:

            raw_keywords = []


        keywords = []


        for item in raw_keywords:


            if isinstance(item, str):

                cleaned_keyword = item.strip()


                if cleaned_keyword:

                    keywords.append(
                        cleaned_keyword
                    )


            elif isinstance(item, dict):


                keyword = (

                    item.get("keyword")

                    or item.get("text")

                    or item.get("name")

                    or item.get("term")

                    or ""

                )


                if isinstance(
                    keyword,
                    str
                ):


                    keyword = keyword.strip()


                    if keyword:

                        keywords.append(
                            keyword
                        )


            else:


                try:


                    keyword = str(item).strip()


                    if keyword:

                        keywords.append(
                            keyword
                        )


                except Exception:

                    pass


        # Remove duplicate keywords

        keywords = list(
            dict.fromkeys(keywords)
        )


        print(
            f"Normalized Keywords: {keywords}"
        )


        # =================================================
        # CREATE QUERY PAPER
        # =================================================

        query_paper = {

            "title":
                title or "",

            "abstract":
                abstract or "",

            "keywords":
                keywords

        }


        research_gap_result = (

            research_gap_service.detect_gap(
                query_paper
            )

        )


        if research_gap_result is None:

            research_gap_result = {}


        print(
            "Research gap detection completed."
        )


        # =================================================
        # STEP 13: PREPARE DATABASE VALUES
        # =================================================

        print(
            "\nSTEP 13: Preparing database values..."
        )


        responsible_score = (

            extract_responsible_score(
                responsible_metrics_result
            )

        )


        responsible_rating = (

            extract_responsible_rating(
                responsible_metrics_result
            )

        )


        compliance_score = safe_float(

            principle_analysis.get(
                "compliance_score"
            )

        )


        if compliance_score is None:


            compliance_score = safe_float(

                principle_analysis.get(
                    "overall_score"
                )

            )


        novelty_level = (

            research_gap_result.get(
                "novelty_level"
            )

        )


        average_similarity = safe_float(

            research_gap_result.get(
                "average_similarity"
            )

        )


        print(
            f"Responsible Score: {responsible_score}"
        )


        print(
            f"Compliance Score: {compliance_score}"
        )


        print(
            f"Novelty Level: {novelty_level}"
        )


        # =================================================
        # STEP 14: SAVE TO DATABASE
        # =================================================

        print(
            "\nSTEP 14: Saving analysis to database..."
        )


        paper_record = Paper(


            # FILE INFORMATION

            file_id=file_id,

            file_hash=file_hash,

            filename=original_filename,

            title=title,


            # PAPER STATISTICS

            page_count=pdf_data.get(
                "page_count"
            ),

            word_count=pdf_data.get(
                "word_count"
            ),

            character_count=pdf_data.get(
                "character_count"
            ),


            # RESPONSIBLE METRICS

            responsible_score=responsible_score,

            responsible_rating=responsible_rating,


            # PRINCIPLE ANALYSIS

            compliance_score=compliance_score,


            # RESEARCH GAP

            novelty_level=novelty_level,

            average_similarity=average_similarity,


            # COMPLETE ANALYSIS RESULTS

            nlp_analysis=safe_json_dumps(
                nlp_analysis
            ),


            bibliometric_analysis=safe_json_dumps(
                bibliometric_data
            ),


            responsible_metrics_analysis=safe_json_dumps(
                responsible_metrics_result
            ),


            principle_analysis=safe_json_dumps(
                principle_analysis
            ),


            research_gap_analysis=safe_json_dumps(
                research_gap_result
            ),


            # MULTI-LEVEL FRAMEWORK

            multi_level_analysis=safe_json_dumps(
                multi_level_analysis
            )

        )


        db.add(
            paper_record
        )


        db.commit()


        db.refresh(
            paper_record
        )


        print(
            "Database save completed successfully."
        )


        print(
            f"Database ID: {paper_record.id}"
        )


        # =================================================
        # STEP 15: COMPLETE ANALYSIS RESPONSE
        # =================================================

        print("\n")

        print("=" * 70)

        print(
            "PAPER ANALYSIS COMPLETED SUCCESSFULLY"
        )

        print("=" * 70)

        print("\n")


        return {


            "message":

                "Complete research paper analysis "
                "completed successfully",


            "database_id":

                paper_record.id,


            # FILE INFORMATION

            "file": {

                "file_id":
                    file_id,

                "filename":
                    original_filename

            },


            # PAPER INFORMATION

            "paper_information": {

                "detected_title":
                    title,

                "page_count":

                    pdf_data.get(
                        "page_count",
                        0
                    ),

                "word_count":

                    pdf_data.get(
                        "word_count",
                        0
                    ),

                "character_count":

                    pdf_data.get(
                        "character_count",
                        0
                    )

            },


            # DETECTED SECTIONS

            "sections_detected":

                list(
                    sections.keys()
                ),


            # NLP ANALYSIS

            "nlp_analysis":

                nlp_analysis,


            # BIBLIOMETRIC ANALYSIS

            "bibliometric_analysis":

                bibliometric_data,


            # RESPONSIBLE METRICS

            "responsible_metrics_evaluation":

                responsible_metrics_result,


            # PRINCIPLE ANALYSIS

            "principle_analysis":

                principle_analysis,


            # MULTI-LEVEL FRAMEWORK

            "multi_level_framework":

                multi_level_analysis,


            # RESEARCH GAP ANALYSIS

            "research_gap_analysis":

                research_gap_result

        }


    # =====================================================
    # HANDLE FASTAPI ERRORS
    # =====================================================

    except HTTPException:


        print(
            "\nHTTP Exception occurred during analysis."
        )


        raise


    # =====================================================
    # HANDLE UNEXPECTED ERRORS
    # =====================================================

    except Exception as error:


        try:

            db.rollback()

        except Exception:

            pass


        print("\n")

        print("=" * 80)

        print(
            "ERROR IN PAPER ANALYSIS PIPELINE"
        )

        print("=" * 80)


        print(

            f"ERROR TYPE: "
            f"{type(error).__name__}"

        )


        print(

            f"ERROR MESSAGE: "
            f"{str(error)}"

        )


        print("\nFULL TRACEBACK:\n")


        traceback.print_exc()


        print("\n")

        print("=" * 80)

        print(
            "END OF ERROR TRACEBACK"
        )

        print("=" * 80)

        print("\n")


        raise HTTPException(

            status_code=500,

            detail={

                "error_type":

                    type(error).__name__,


                "message":

                    str(error)

            }

        )