from random import choice

import pytest
from fastapi.testclient import TestClient

from main import app
from ocrlogic.image_utils import open_static_image
from utils.config import IMG_ROUTES

client = TestClient(app)


@pytest.mark.asyncio
async def test_ocrcore_supported_lang_param():
    img_path = choice(IMG_ROUTES)
    lang = "spa"
    with open_static_image(img_path) as img:
        img_name = img.split("/")[-1]
        files = [("images", (img_name, open(img, "rb"), "image/jpeg"))]
        response = client.post("/ocr/images", files=files, params={"lang": lang})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert isinstance(response.json().get(img_name), list)


@pytest.mark.asyncio
async def test_multiple_images():
    img_paths = IMG_ROUTES[:2]
    lang = "eng"
    files = []
    for img_path in img_paths:
        with open_static_image(img_path) as img:
            img_name = img.split("/")[-1]
            files.append(("images", (img_name, open(img, "rb"), "image/jpeg")))
    response = client.post("/ocr/images", files=files, params={"lang": lang})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_ocrcore_invalid_lang_param():
    img_path = choice(IMG_ROUTES)
    lang = "gerrrr"
    with open_static_image(img_path) as img:
        img_name = img.split("/")[-1]
        files = [("images", (img_name, open(img, "rb"), "image/jpeg"))]
        response = client.post("/ocr/images", files=files, params={"lang": lang})

    assert response.status_code == 400
    assert response.json() == {
        "detail": f"Language {lang} not supported. Please choose between 'eng' or 'spa'."
    }
