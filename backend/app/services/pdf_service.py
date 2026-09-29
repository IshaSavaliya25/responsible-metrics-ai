import fitz
import re


class PDFService:

    """
    Service responsible for:

    - Reading PDF files
    - Extracting text
    - Counting pages
    - Detecting research paper sections
    """


    # ==========================================
    # SECTION PATTERNS
    # ==========================================

    SECTION_PATTERNS = {

        "abstract": [

            r"^abstract$",
            r"^summary$"
        ],


        "introduction": [

            r"^1\.?\s*introduction$",
            r"^introduction$",
            r"^background$"
        ],


        "literature_review": [

            r"^literature review$",
            r"^related work$",
            r"^background and literature review$",
            r"^state of the art$"
        ],


        "methodology": [

            r"^methodology$",
            r"^methods$",
            r"^materials and methods$",
            r"^research methodology$",
            r"^research methods$",
            r"^methodological approach$",
            r"^method$"
        ],


        "results": [

            r"^results$",
            r"^findings$",
            r"^research findings$",
            r"^empirical results$",
            r"^analysis and results$"
        ],


        "discussion": [

            r"^discussion$",
            r"^results and discussion$",
            r"^discussion and implications$"
        ],


        "conclusion": [

            r"^conclusion$",
            r"^conclusions$",
            r"^concluding remarks$",
            r"^conclusion and future work$",
            r"^summary and conclusion$"
        ],


        "references": [

            r"^references$",
            r"^bibliography$",
            r"^reference list$"
        ]

    }


    # ==========================================
    # EXTRACT COMPLETE PDF TEXT
    # ==========================================

    @staticmethod
    def extract_text(file_path: str):

        document = fitz.open(
            file_path
        )


        full_text = ""

        page_count = len(
            document
        )


        for page in document:

            page_text = page.get_text(

                "text"

            )

            full_text += page_text + "\n"


        document.close()


        full_text = re.sub(

            r"\n{3,}",

            "\n\n",

            full_text

        )


        sections = PDFService.detect_sections(
            full_text
        )


        word_count = len(
            full_text.split()
        )


        character_count = len(
            full_text
        )


        return {

            "text": full_text,

            "sections": sections,

            "page_count": page_count,

            "word_count": word_count,

            "character_count": character_count

        }


    # ==========================================
    # NORMALIZE HEADING
    # ==========================================

    @staticmethod
    def normalize_heading(text: str):

        text = text.strip()

        text = text.lower()


        # Remove numbering like:
        # 1 Introduction
        # 1.1 Methodology
        # II. Results

        text = re.sub(

            r"^(?:\d+[\.\d]*|[ivxlcdm]+)[\.\)]?\s*",

            "",

            text

        )


        # Remove extra symbols

        text = re.sub(

            r"[^a-z\s]",

            "",

            text

        )


        text = re.sub(

            r"\s+",

            " ",

            text

        ).strip()


        return text


    # ==========================================
    # CHECK IF LINE IS SECTION HEADING
    # ==========================================

    @staticmethod
    def detect_heading(line: str):

        normalized_line = PDFService.normalize_heading(
            line
        )


        if not normalized_line:

            return None


        for section, patterns in PDFService.SECTION_PATTERNS.items():

            for pattern in patterns:

                if re.match(

                    pattern,

                    normalized_line,

                    re.IGNORECASE

                ):

                    return section


        return None


    # ==========================================
    # DETECT SECTIONS
    # ==========================================

    @staticmethod
    def detect_sections(text: str):

        lines = text.splitlines()


        sections = {}


        current_section = "unknown"


        sections[current_section] = []


        for line in lines:

            stripped_line = line.strip()


            if not stripped_line:

                continue


            detected_section = (

                PDFService.detect_heading(

                    stripped_line

                )

            )


            # ----------------------------------
            # NEW SECTION DETECTED
            # ----------------------------------

            if detected_section:

                current_section = detected_section


                if current_section not in sections:

                    sections[current_section] = []


                continue


            # ----------------------------------
            # ADD CONTENT TO CURRENT SECTION
            # ----------------------------------

            sections[

                current_section

            ].append(

                stripped_line

            )


        # ======================================
        # CONVERT LISTS TO TEXT
        # ======================================

        cleaned_sections = {}


        for section_name, content in sections.items():

            section_text = " ".join(
                content
            )


            if section_text.strip():

                cleaned_sections[
                    section_name
                ] = section_text


        # ======================================
        # REMOVE REFERENCES FROM NLP CONTENT
        # ======================================

        if "references" in cleaned_sections:

            # References are detected but retained.
            # NLP service can ignore them.

            pass


        return cleaned_sections