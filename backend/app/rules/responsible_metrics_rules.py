"""
Formalized Rules and Guidelines for Responsible Use of Bibliometric Indicators
Derived from:
1. The Leiden Manifesto for Research Metrics (Hicks et al., Nature 2015)
2. The San Francisco Declaration on Research Assessment (DORA, 2012)
3. The Hong Kong Principles for assessing researchers (Moher et al., PLOS Bio 2020)
4. INORMS SCOPE Framework
"""

LEIDEN_PRINCIPLES = {
    "LP1": {
        "title": "Quantitative evaluation that supports qualitative, expert assessment",
        "description": "Metrics must never supplant qualitative judgment; quantitative metrics inform peer review, not replace it.",
        "keywords": ["qualitative assessment", "expert judgment", "peer review", "human judgment", "complements peer review"]
    },
    "LP2": {
        "title": "Measure performance against research missions",
        "description": "Evaluation goals must align with institutional, regional, or departmental strategic priorities.",
        "keywords": ["institutional mission", "research mission", "strategic goals", "departmental context"]
    },
    "LP3": {
        "title": "Protect excellence in locally relevant research",
        "description": "Ensure research published in local languages or addressing regional problems is not penalized by global English-biased indexes.",
        "keywords": ["locally relevant", "regional context", "local language", "societal impact"]
    },
    "LP4": {
        "title": "Keep data collection and analytical processes open, transparent, and simple",
        "description": "Data sources and calculation formulas must be accessible, reproducible, and verifiable.",
        "keywords": ["transparent", "open data", "reproducibility", "reproducible", "open methodology", "openalex", "crossref"]
    },
    "LP5": {
        "title": "Allow those evaluated to verify data and analysis",
        "description": "Researchers and institutions must have the opportunity to review, contest, and correct citation inaccuracies.",
        "keywords": ["data verification", "auditable", "verify data", "dispute resolution"]
    },
    "LP6": {
        "title": "Account for variation by field in publication and citation practices",
        "description": "Citation rates vary drastically by discipline; field-weighted normalization (e.g. FWCI) is mandatory.",
        "keywords": ["field normalization", "disciplinary differences", "disciplinary context", "field-weighted", "fwci", "subject category"]
    },
    "LP7": {
        "title": "Base assessment of individual researchers on qualitative judgment of their portfolio",
        "description": "Cumulative lifelong metrics (such as h-index) must not dictate individual career, hiring, or promotion assessments.",
        "keywords": ["portfolio assessment", "holistic evaluation", "career stage", "early career", "qualitative portfolio"]
    },
    "LP8": {
        "title": "Avoid misplaced concreteness and false precision",
        "description": "Indicators are prone to conceptual ambiguity; reporting metrics to 3 decimal places gives an illusion of precision.",
        "keywords": ["false precision", "uncertainty", "confidence intervals", "robustness"]
    },
    "LP9": {
        "title": "Recognize the systemic gaming effects of assessment and indicators",
        "description": "Goodhart's law: When a metric becomes a target, it ceases to be a good metric (e.g., citation cartels, salami slicing).",
        "keywords": ["gaming", "goodhart", "unintended consequences", "citation cartels", "metric distortion"]
    },
    "LP10": {
        "title": "Scrutinize indicators regularly and update them",
        "description": "Evaluation regimes must be periodically reviewed and adjusted to remain effective.",
        "keywords": ["regular review", "periodic review", "updating indicators", "indicator lifecycle"]
    }
}

DORA_PRINCIPLES = {
    "DORA1": {
        "title": "Do not use journal-based metrics as a surrogate measure of the quality of individual research articles",
        "description": "Journal Impact Factor (JIF) measures the journal, not the paper; articles must be judged on scientific content.",
        "keywords": ["do not use journal impact factor", "avoid jif", "article-level metrics", "content evaluation"]
    },
    "DORA2": {
        "title": "Assess research based on its own merits rather than the journal in which it was published",
        "description": "Value all research outputs (datasets, software, protocols) in addition to conventional journal papers.",
        "keywords": ["datasets", "software", "research outputs", "intrinsic merit", "preprints"]
    },
    "DORA3": {
        "title": "Highlight open access and data transparency in evaluation",
        "description": "Promote fair, accessible, and inclusive scholarly communication.",
        "keywords": ["open access", "open science", "data sharing", "fair access"]
    }
}

# Concrete Misuse Patterns & Violations
MISUSE_RULES = [
    {
        "id": "MISUSE_JIF_INDIVIDUAL",
        "framework": "DORA & Leiden Principle 7",
        "severity": "HIGH",
        "name": "Journal Impact Factor Applied to Individual Article or Researcher",
        "regex_patterns": [
            r"(evaluated|judged|ranked|selected)\s+(solely|primarily)?\s*(based on|by)\s*(the\s+)?(journal\s+)?impact\s+factor",
            r"high\s+impact\s+factor\s+proves\s+(the\s+)?quality",
            r"jif\s+(of|threshold|cutoff)\s+was\s+used\s+to\s+(hire|promote|evaluate)"
        ],
        "explanation": "Using Journal Impact Factor to judge an individual article or researcher violates DORA Principle 1 and Leiden Principle 7. Citation distribution in any journal is heavily skewed (top 20% generate 80% of citations).",
        "remediation": "Replace JIF with article-level metrics (e.g. Field-Weighted Citation Impact, percentile benchmarks) and peer evaluation of scientific rigor."
    },
    {
        "id": "MISUSE_UNNORMALIZED_COMPARISON",
        "framework": "Leiden Principle 6",
        "severity": "HIGH",
        "name": "Direct Unnormalized Cross-Discipline Comparison",
        "regex_patterns": [
            r"compared\s+citations\s+across\s+(different\s+)?fields\s+without\s+normalization",
            r"raw\s+citation\s+counts?\s+(were|was)\s+used\s+to\s+compare\s+departments",
            r"higher\s+citation\s+count\s+proves\s+superiority\s+across\s+disciplines"
        ],
        "explanation": "Comparing raw citations across disparate disciplines is invalid. Molecular biology articles naturally accumulate 5x-10x more citations than mathematics or humanities papers.",
        "remediation": "Apply field-normalization techniques (e.g., Mean Normalized Citation Score - MNCS, or Scopus FWCI) and compare within normalized percentiles."
    },
    {
        "id": "MISUSE_HINDEX_CUTOFF",
        "framework": "Leiden Principle 7",
        "severity": "MEDIUM",
        "name": "Arbitrary h-index Cutoff for Personnel Decisions",
        "regex_patterns": [
            r"h-index\s*(threshold|cutoff|minimum)\s+(of\s+\d+|for\s+(tenure|hiring|promotion))",
            r"candidates\s+with\s+h-index\s+below\s+\d+\s+were\s+excluded"
        ],
        "explanation": "The h-index is inherently dependent on career length and disciplinary citation density. Imposing rigid cutoffs systematically discriminates against early-career researchers, women taking parental leaves, and researchers in smaller fields.",
        "remediation": "Adopt narrative CVs (e.g. Résumé for Research and Innovation - R4RI) and age-adjusted metrics like m-quotient alongside qualitative contributions."
    },
    {
        "id": "MISUSE_FALSE_PRECISION",
        "framework": "Leiden Principle 8",
        "severity": "LOW",
        "name": "False Precision / Misplaced Concreteness",
        "regex_patterns": [
            r"impact\s+factor\s+of\s+\d+\.\d{3,}",
            r"calculated\s+to\s+\d+\s+decimal\s+places\s+to\s+distinguish"
        ],
        "explanation": "Reporting bibliometric metrics to three decimal places creates a fraudulent sense of scientific certainty.",
        "remediation": "Report bibliometric indicators as rounded values or confidence intervals to reflect underlying sampling variability."
    }
]

def get_remediation_recommendations(detected_misuses: list, compliance_score: float) -> list:
    """Generate prioritized actionable recommendations based on detected practices."""
    recommendations = []

    for misuse in detected_misuses:
        recommendations.append({
            "priority": misuse.get("severity", "MEDIUM"),
            "target": misuse.get("name", "Indicator Use"),
            "action": misuse.get("remediation", "Adopt contextual qualitative assessment.")
        })

    if compliance_score < 50.0:
        recommendations.append({
            "priority": "HIGH",
            "target": "Overall Compliance",
            "action": "Adopt a multi-dimensional assessment matrix combining quantitative indicators with narrative peer review portfolios."
        })

    if not any(m.get("id") == "MISUSE_UNNORMALIZED_COMPARISON" for m in detected_misuses):
        recommendations.append({
            "priority": "LOW",
            "target": "Field Normalization",
            "action": "Ensure all citation-based comparisons across cohorts use subject-normalized indicators (e.g., FWCI or OpenAlex percentiles)."
        })

    return recommendations
