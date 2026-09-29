import re


class SectionService:

    # Different possible names for research paper sections
    SECTION_PATTERNS = {
        "abstract": [
            "abstract"
        ],

        "introduction": [
            "introduction",
            "1 introduction"
        ],

        "literature_review": [
            "literature review",
            "related work",
            "background"
        ],

        "methodology": [
            "methodology",
            "methods",
            "method",
            "materials and methods",
            "research methodology",
            "proposed methodology"
        ],

        "results": [
            "results",
            "experimental results",
            "experiments",
            "evaluation"
        ],

        "discussion": [
            "discussion",
            "results and discussion"
        ],

        "conclusion": [
            "conclusion",
            "conclusions",
            "concluding remarks",
            "summary and conclusion"
        ],

        "references": [
            "references",
            "bibliography"
        ]
    }


    @staticmethod
    def normalize_heading(text: str) -> str:
        """
        Normalize a possible section heading.
        """

        text = text.lower().strip()

        # Remove numbering like:
        # 1. Introduction
        # 1 Introduction
        # I. Introduction
        text = re.sub(
            r"^[\divxlcdm]+[\.\)]?\s+",
            "",
            text,
            flags=re.IGNORECASE
        )

        return text.strip()


    @classmethod
    def identify_heading(cls, line: str):
        """
        Identify whether a line matches a known section heading.
        """

        normalized_line = cls.normalize_heading(line)

        for section, patterns in cls.SECTION_PATTERNS.items():

            for pattern in patterns:

                if normalized_line == pattern:
                    return section

        return None


    @classmethod
    def detect_sections(cls, text: str) -> dict:
        """
        Detect and separate sections from research paper text.
        """

        lines = text.split("\n")

        sections = {}

        current_section = "unknown"

        sections[current_section] = []

        for line in lines:

            stripped_line = line.strip()

            if not stripped_line:
                continue

            detected_section = cls.identify_heading(
                stripped_line
            )

            if detected_section:

                current_section = detected_section

                if current_section not in sections:
                    sections[current_section] = []

            else:

                sections[current_section].append(
                    stripped_line
                )

        # Convert list content to strings
        formatted_sections = {}

        for section_name, content in sections.items():

            formatted_sections[section_name] = "\n".join(
                content
            )

        return formatted_sections