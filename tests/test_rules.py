import pytest
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.rules.responsible_metrics_rules import (
    LEIDEN_PRINCIPLES,
    DORA_PRINCIPLES,
    MISUSE_RULES,
    get_remediation_recommendations
)
from app.services.principle_detection_service import PrincipleDetectionService


def test_leiden_principles_defined():
    """Verify that all 10 Leiden Principles are formally defined."""
    assert len(LEIDEN_PRINCIPLES) == 10
    for key in [f"LP{i}" for i in range(1, 11)]:
        assert key in LEIDEN_PRINCIPLES
        assert "title" in LEIDEN_PRINCIPLES[key]
        assert "description" in LEIDEN_PRINCIPLES[key]
        assert len(LEIDEN_PRINCIPLES[key]["keywords"]) > 0


def test_dora_principles_defined():
    """Verify DORA recommendation definitions."""
    assert len(DORA_PRINCIPLES) >= 3
    for key, val in DORA_PRINCIPLES.items():
        assert "title" in val
        assert "description" in val or "target" in val
        assert len(val["keywords"]) > 0


def test_misuse_rules_defined():
    """Verify misuse rules definitions and remediation guidance."""
    assert len(MISUSE_RULES) >= 4
    for rule_info in MISUSE_RULES:
        assert "id" in rule_info
        assert "severity" in rule_info
        assert "remediation" in rule_info
        assert len(rule_info["regex_patterns"]) > 0


def test_remediation_lookup():
    """Verify remediation lookup handles known and unknown codes."""
    rec = get_remediation_recommendations([MISUSE_RULES[0]], compliance_score=50)
    assert len(rec) >= 1
    assert "action" in rec[0]

    # Empty list
    empty_rec = get_remediation_recommendations([], compliance_score=90)
    assert isinstance(empty_rec, list)


def test_principle_detection_service_basic():
    """Test PrincipleDetectionService detection logic on sample text."""
    service = PrincipleDetectionService()
    text = (
        "We emphasize that citation metrics alone cannot replace qualitative expert peer review. "
        "Furthermore, field normalization such as FWCI must be applied across disciplines, "
        "and data sources must remain completely open and transparent."
    )
    result = service.analyze(text)
    assert "compliance_score" in result
    assert "responsible_practices" in result
    assert len(result["responsible_practices"]) > 0
    assert "recommendations" in result
