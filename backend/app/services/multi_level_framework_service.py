class MultiLevelFrameworkService:

    def __init__(self):

        # ==========================================
        # LEVEL 1 — INDICATOR LEVEL
        # ==========================================

        self.indicator_keywords = {

            "citation_metrics": [
                "citation count",
                "citations",
                "citation analysis",
                "citation impact",
                "citation",
                "cited by",
                "metrics",
                "metric"
            ],

            "h_index": [
                "h-index",
                "h index",
                "author metric",
                "author-level metric"
            ],

            "impact_factor": [
                "impact factor",
                "journal impact factor",
                "jif",
                "journal ranking",
                "journal metrics"
            ],

            "altmetrics": [
                "altmetrics",
                "alternative metrics",
                "social media metrics",
                "views",
                "downloads",
                "readers"
            ],

            "limitations": [
                "limitation",
                "limitations",
                "bias",
                "context",
                "misuse",
                "shortcoming",
                "weakness",
                "boundary"
            ]
        }


        # ==========================================
        # LEVEL 2 — RESEARCHER LEVEL
        # ==========================================

        self.researcher_keywords = {

            "individual_evaluation": [
                "researcher",
                "individual researcher",
                "scientist",
                "academic",
                "author",
                "investigator",
                "practitioner"
            ],

            "career_context": [
                "career stage",
                "early career",
                "senior researcher",
                "research career",
                "phd student",
                "postdoc",
                "career"
            ],

            "qualitative_evaluation": [
                "peer review",
                "qualitative assessment",
                "expert judgement",
                "expert judgment",
                "narrative",
                "qualitative",
                "peer-reviewed",
                "reviewer"
            ],

            "fairness": [
                "fairness",
                "fair evaluation",
                "responsible evaluation",
                "equity",
                "ethics",
                "unbiased",
                "fair"
            ]
        }


        # ==========================================
        # LEVEL 3 — INSTITUTIONAL LEVEL
        # ==========================================

        self.institution_keywords = {

            "institutional_evaluation": [
                "institution",
                "university",
                "research organization",
                "research institution",
                "department",
                "laboratory",
                "faculty",
                "institute"
            ],

            "disciplinary_context": [
                "disciplinary context",
                "discipline",
                "field differences",
                "field normalization",
                "domain",
                "subject area",
                "interdisciplinary"
            ],

            "multiple_indicators": [
                "multiple indicators",
                "multidimensional",
                "multi-dimensional",
                "combination of indicators",
                "holistic",
                "diverse indicators",
                "multi-level"
            ],

            "institutional_comparison": [
                "institutional comparison",
                "ranking",
                "university ranking",
                "benchmark",
                "benchmarking",
                "comparison"
            ]
        }


        # ==========================================
        # LEVEL 4 — SYSTEM / POLICY LEVEL
        # ==========================================

        self.system_keywords = {

            "transparency": [
                "transparency",
                "transparent",
                "open methodology",
                "reproducibility",
                "reproducible",
                "open access",
                "open data",
                "publicly available",
                "open science"
            ],

            "policy": [
                "research policy",
                "evaluation policy",
                "policy framework",
                "policy",
                "guidelines",
                "regulations",
                "protocols"
            ],

            "governance": [
                "governance",
                "stakeholders",
                "decision making",
                "oversight",
                "standardization",
                "management",
                "stewardship"
            ],

            "responsible_principles": [
                "responsible metrics",
                "leiden manifesto",
                "dora",
                "responsible research assessment",
                "responsible",
                "principles",
                "best practices"
            ]
        }


    # ==========================================
    # MAIN ANALYSIS FUNCTION
    # ==========================================

    def analyze(
        self,
        text
    ):
        if isinstance(text, dict):
            text = text.get("text", "")

        if not text or not isinstance(text, str):
            return {
                "overall_score": 0,
                "overall_rating": "Unknown",
                "levels": {}
            }

        text_lower = text.lower()

        # Analyze all framework levels
        indicator_result = self.evaluate_level(
            text_lower,
            self.indicator_keywords
        )

        researcher_result = self.evaluate_level(
            text_lower,
            self.researcher_keywords
        )

        institution_result = self.evaluate_level(
            text_lower,
            self.institution_keywords
        )

        system_result = self.evaluate_level(
            text_lower,
            self.system_keywords
        )

        # ==========================================
        # CALCULATE OVERALL SCORE
        # ==========================================

        scores = [
            indicator_result["score"],
            researcher_result["score"],
            institution_result["score"],
            system_result["score"]
        ]

        overall_score = round(
            sum(scores) / len(scores),
            2
        )

        overall_rating = self.get_rating(
            overall_score
        )

        return {
            "overall_score": overall_score,
            "overall_rating": overall_rating,
            "levels": {
                "indicator_level": indicator_result,
                "researcher_level": researcher_result,
                "institutional_level": institution_result,
                "system_policy_level": system_result
            }
        }


    # ==========================================
    # EVALUATE INDIVIDUAL LEVEL
    # ==========================================

    def evaluate_level(
        self,
        text,
        categories
    ):
        import re

        matched_categories = []
        matched_keywords = []
        total_categories = len(categories)

        for category, keywords in categories.items():
            category_found = False

            for keyword in keywords:
                kw_lower = keyword.lower()
                # Fast substring or word boundary match
                if " " in kw_lower:
                    found = kw_lower in text
                else:
                    found = bool(re.search(r"\b" + re.escape(kw_lower) + r"\b", text))

                if found:
                    matched_keywords.append(keyword)
                    category_found = True

            if not category_found:
                # Semantic check if exact keywords missing
                try:
                    from app.ml.embeddings import EmbeddingService
                    emb_service = EmbeddingService()
                    if not emb_service._use_fallback and emb_service._model is not None:
                        cat_query = f"{category.replace('_', ' ')}: {' '.join(keywords[:3])}"
                        text_sample = text[:2000]
                        sim = emb_service.compute_similarity(cat_query, text_sample)
                        if sim >= 0.55:
                            category_found = True
                            matched_keywords.append(f"{category} (semantic match)")
                except Exception:
                    pass

            if category_found:
                matched_categories.append(category)

        score = round(
            (len(matched_categories) / total_categories) * 100,
            2
        )

        rating = self.get_rating(score)

        return {
            "score": score,
            "rating": rating,
            "matched_categories": matched_categories,
            "matched_keywords": list(set(matched_keywords)),
            "coverage": f"{len(matched_categories)}/{total_categories}"
        }


    # ==========================================
    # SCORE RATING
    # ==========================================

    def get_rating(

        self,

        score

    ):


        if score >= 80:

            return "Excellent"


        elif score >= 60:

            return "Good"


        elif score >= 40:

            return "Moderate"


        elif score >= 20:

            return "Low"


        return "Very Low"