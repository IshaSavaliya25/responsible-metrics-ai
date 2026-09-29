import re


class ResponsibleMetricsService:

    """
    Service for evaluating responsible use of
    bibliometric indicators.

    The evaluation is based on six dimensions:

    1. Contextual Evaluation
    2. Transparency
    3. Metric Diversity
    4. Qualitative Evidence
    5. Discipline Awareness
    6. Limitations Awareness
    """


    def __init__(self):

        self.dimensions = {

            "contextual_evaluation": {

                "weight": 20,

                "keywords": [

                    "context",
                    "contextual",
                    "research context",
                    "evaluation context",
                    "appropriate use",
                    "responsible use",
                    "tailored",
                    "purpose",
                    "goals",
                    "level of analysis"
                ]
            },


            "transparency": {

                "weight": 15,

                "keywords": [

                    "transparent",
                    "transparency",
                    "open",
                    "openness",
                    "reproducible",
                    "reproducibility",
                    "methodological transparency",
                    "data availability",
                    "documentation"
                ]
            },


            "metric_diversity": {

                "weight": 15,

                "keywords": [

                    "multiple indicators",
                    "multiple metrics",
                    "multidimensional",
                    "diverse indicators",
                    "combination of indicators",
                    "quantitative and qualitative",
                    "mixed methods",
                    "complementary indicators"
                ]
            },


            "qualitative_evidence": {

                "weight": 15,

                "keywords": [

                    "peer review",
                    "qualitative",
                    "expert judgement",
                    "expert judgment",
                    "narrative",
                    "qualitative evidence",
                    "human judgement",
                    "human judgment"
                ]
            },


            "discipline_awareness": {

                "weight": 15,

                "keywords": [

                    "discipline",
                    "disciplinary",
                    "field differences",
                    "research field",
                    "field-specific",
                    "disciplinary context",
                    "subject area",
                    "domain-specific"
                ]
            },


            "limitations_awareness": {

                "weight": 20,

                "keywords": [

                    "limitation",
                    "limitations",
                    "bias",
                    "misuse",
                    "misinterpretation",
                    "caution",
                    "care",
                    "responsible",
                    "inappropriate",
                    "problem",
                    "risk"
                ]
            }

        }


    # ==========================================
    # CLEAN TEXT
    # ==========================================

    def clean_text(self, text):

        if not text:

            return ""

        text = text.lower()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text


    # ==========================================
    # COUNT KEYWORD MATCHES
    # ==========================================

    def calculate_dimension_score(
        self,
        text,
        keywords
    ):

        text = self.clean_text(text)

        if not text:

            return {

                "score": 0,

                "matched_keywords": [],

                "match_count": 0
            }


        matched_keywords = []


        for keyword in keywords:

            if keyword.lower() in text:

                matched_keywords.append(
                    keyword
                )


        match_count = len(
            matched_keywords
        )


        # Maximum matches required
        # for full dimension score

        max_matches = max(

            3,

            int(
                len(keywords) * 0.3
            )
        )


        raw_score = (

            match_count /
            max_matches

        ) * 100


        score = min(

            round(
                raw_score,
                2
            ),

            100
        )


        return {

            "score": score,

            "matched_keywords":
                matched_keywords,

            "match_count":
                match_count
        }


    # ==========================================
    # BUILD COMPLETE TEXT
    # ==========================================

    def build_analysis_text(
        self,
        sections,
        nlp_analysis
    ):

        text_parts = []


        # Paper sections

        if sections:

            for value in sections.values():

                if isinstance(value, str):

                    text_parts.append(
                        value
                    )


        # NLP findings

        if nlp_analysis:

            for key, value in nlp_analysis.items():

                if isinstance(value, str):

                    text_parts.append(
                        value
                    )


                elif isinstance(value, list):

                    for item in value:

                        if isinstance(item, str):

                            text_parts.append(
                                item
                            )


                        elif isinstance(item, dict):

                            text_parts.append(
                                str(item)
                            )


        return " ".join(
            text_parts
        )


    # ==========================================
    # EVALUATE RESPONSIBLE METRICS
    # ==========================================

    def evaluate(
        self,
        bibliometric_data=None,
        nlp_analysis=None,
        sections=None
    ):

        bibliometric_data = (
            bibliometric_data or {}
        )

        nlp_analysis = (
            nlp_analysis or {}
        )

        sections = (
            sections or {}
        )


        # Build paper text

        analysis_text = (

            self.build_analysis_text(

                sections,

                nlp_analysis

            )

        )


        dimension_results = {}


        weighted_score = 0


        # ======================================
        # ANALYZE EACH DIMENSION
        # ======================================

        for dimension, config in self.dimensions.items():

            result = (

                self.calculate_dimension_score(

                    analysis_text,

                    config["keywords"]

                )

            )


            dimension_score = result[
                "score"
            ]


            weight = config[
                "weight"
            ]


            weighted_contribution = (

                dimension_score *

                (weight / 100)

            )


            weighted_score += (

                weighted_contribution
            )


            dimension_results[
                dimension
            ] = {

                "score":
                    dimension_score,

                "weight":
                    weight,

                "weighted_contribution":

                    round(
                        weighted_contribution,
                        2
                    ),

                "matched_keywords":

                    result[
                        "matched_keywords"
                    ],

                "match_count":

                    result[
                        "match_count"
                    ]
            }


        # ======================================
        # BIBLIOMETRIC BONUS
        # ======================================

        bibliometric_bonus = 0


        if bibliometric_data:

            if bibliometric_data.get(
                "citation_count"
            ) is not None:

                bibliometric_bonus += 2


            if bibliometric_data.get(
                "publication_year"
            ):

                bibliometric_bonus += 1


            if bibliometric_data.get(
                "open_access"
            ):

                bibliometric_bonus += 2


        # Maximum bonus = 5

        bibliometric_bonus = min(

            bibliometric_bonus,

            5
        )


        # ======================================
        # FINAL SCORE
        # ======================================

        final_score = min(

            round(
                weighted_score +
                bibliometric_bonus,
                2
            ),

            100
        )


        # ======================================
        # DETERMINE RATING
        # ======================================

        if final_score >= 80:

            rating = (
                "Excellent Responsible Practice"
            )


        elif final_score >= 65:

            rating = (
                "Good Responsible Practice"
            )


        elif final_score >= 50:

            rating = (
                "Moderate Responsible Practice"
            )


        elif final_score >= 30:

            rating = (
                "Limited Responsible Practice"
            )


        else:

            rating = (
                "Poor Responsible Practice"
            )


        # ======================================
        # RETURN RESULT
        # ======================================

        return {

            "overall": {

                "responsible_metrics_score":

                    final_score,

                "rating":

                    rating,

                "bibliometric_bonus":

                    bibliometric_bonus

            },


            "dimensions":

                dimension_results

        }