import sys
import os
import pytest
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.ml.embeddings import EmbeddingService
from app.ml.classifier import MetricStanceClassifier


def test_embedding_service_singleton_and_encode():
    """Verify EmbeddingService encodes strings to 384-dimensional normalized vectors."""
    service1 = EmbeddingService()
    service2 = EmbeddingService()
    assert service1 is service2

    vec = service1.encode("Scientometric evaluation using Leiden manifesto principles.")
    assert isinstance(vec, np.ndarray)
    assert vec.shape == (384,)

    # Norm should be approximately 1.0 (normalized vector)
    norm = np.linalg.norm(vec)
    assert 0.95 <= norm <= 1.05


def test_embedding_service_similarity():
    """Verify semantic similarity calculation."""
    service = EmbeddingService()
    sim_high = service.compute_similarity(
        "Journal impact factor should not evaluate individual researchers.",
        "DORA states impact factors cannot measure individual researcher merit."
    )
    sim_low = service.compute_similarity(
        "Journal impact factor should not evaluate individual researchers.",
        "Deep convolutional neural networks for computer vision segmentation."
    )
    assert sim_high > sim_low


def test_metric_stance_classifier():
    """Verify classification of critical awareness vs uncritical reliance."""
    classifier = MetricStanceClassifier()

    critical_text = "We note the severe limitations and bias of raw citation counts, advocating qualitative assessment."
    crit_result = classifier.classify_sentence(critical_text)
    assert crit_result["stance"] == "CRITICAL_AWARE"
    assert crit_result["risk_level"] == "MINIMAL (Good Practice)"

    uncritical_text = "Candidates with an h-index lower than 15 were strictly filtered out of consideration."
    uncrit_result = classifier.classify_sentence(uncritical_text)
    assert uncrit_result["stance"] == "UNCRITICAL_RELIANCE"
    assert "HIGH" in uncrit_result["risk_level"]
