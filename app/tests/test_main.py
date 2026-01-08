from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Ba Zi Destiny" in response.text
    assert "Ba Zi Destiny Reader" in response.text

def test_static_css_exists():
    response = client.get("/static/style.css")
    assert response.status_code == 200

def test_static_js_exists():
    response = client.get("/static/script.js")
    assert response.status_code == 200

# We can't easily test the /predict endpoint fully without mocking the Gemini API,
# but we can test that it handles missing API key gracefully (if we don't set it in env)
# or that it accepts the form data.

def test_predict_endpoint_structure():
    # Sending form data
    response = client.post(
        "/predict",
        data={
            "birthday": "2000-01-01",
            "birth_time": "12:00",
            "location": "Beijing, China"
        }
    )
    # Even if API key is missing, it returns a StreamingResponse with 200 OK
    assert response.status_code == 200
    # The content will be the error message if key is missing, or stream if present.
    # Since we are not setting the key in the test environment explicitly here (or might be missing),
    # we just check status code.
