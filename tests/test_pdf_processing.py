import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.services.pdf_service import PDFService


def test_normalize_heading():
    """Verify heading normalization strips numbers, Roman numerals, and punctuation."""
    test_cases = [
        ("1. Introduction", "introduction"),
        ("1.1 Methodology", "methodology"),
        ("II. Results & Discussion", "results discussion"),
        ("  3. Conclusion and Future Work  ", "conclusion and future work"),
        ("Abstract", "abstract"),
    ]
    for raw, expected in test_cases:
        normalized = PDFService.normalize_heading(raw)
        assert normalized == expected, f"Expected '{expected}' for '{raw}', got '{normalized}'"


def test_detect_sections_from_synthetic_text():
    """Verify that detect_sections parses standard sections."""
    sample_paper = """
Abstract
This paper presents an evaluation of bibliometric indicators in academic assessment.

1. Introduction
Modern research assessment relies heavily on citation counts and impact factors.

2. Related Work
Previous studies have analyzed the distortion caused by Goodhart's law in science.

3. Methodology
We propose a multi-level NLP evaluation framework using sentence transformers.

4. Results
Our empirical results demonstrate high correlation with qualitative peer review.

5. Conclusion
We conclude that responsible metrics principles must be integrated into assessment policies.
"""
    sections = PDFService.detect_sections(sample_paper)
    assert isinstance(sections, dict)
    assert "abstract" in sections
    assert "introduction" in sections
    assert "methodology" in sections
    assert "results" in sections
    assert "conclusion" in sections
    assert len(sections["abstract"]) > 0
