import pytest
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_greetings():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hola mundo"}


@pytest.mark.asyncio
async def test_ocrcore_supported_lang_param():
    img_path = "gran_registro"
    lang = "eng"
    response = await client.post(
        "/ocr",
        json={"img_path": img_path, "lang": lang}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), str)


@pytest.mark.asyncio
async def test_ocrcore_invalid_lang_param():
    img_path = "gran_registro"
    lang = "ger"
    response = await client.post(
        "/ocr",
        json={"img_path": img_path, "lang": lang}
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": f"Language {lang} not supported. Please choose between 'eng' or 'spa'."
    }