import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Verify that root endpoint returns service info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "ResponsibleMetrics AI" in data["message"]


def test_health_check_endpoint():
    """Verify health check returns status healthy."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "healthy"


def test_cors_headers():
    """Verify CORS middleware is properly active on responses."""
    response = client.get(
        "/health",
        headers={"Origin": "http://localhost:8501"}
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") in ["*", "http://localhost:8501"]


def test_principles_analyze_endpoint():
    """Verify the modular principle analysis microservice endpoint."""
    payload = {
        "text": (
            "We adhere to DORA guidelines by avoiding journal impact factors to judge individuals. "
            "Instead, we use qualitative expert review and field-weighted indicators."
        )
    }
    response = client.post("/api/principles/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "analysis" in data
    assert "compliance_score" in data["analysis"]
