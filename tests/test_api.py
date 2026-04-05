import pytest

try:
    from fastapi.testclient import TestClient
    from anima_ew_cruise_missile.serve import app
except Exception as exc:  # pragma: no cover
    app = None
    _import_error = exc


@pytest.mark.skipif(app is None, reason="fastapi not installed")
def test_health_endpoint():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


@pytest.mark.skipif(app is None, reason="fastapi not installed")
def test_predict_endpoint():
    client = TestClient(app)
    resp = client.post("/predict", json={"config": "configs/debug.toml", "episodes": 2, "scenario": "ew_only"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["scenario"] == "ew_only"
    assert data["episodes"] == 2
