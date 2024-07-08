import pytest

from ocrlogic.ocr_core import ocr_core


@pytest.mark.asyncio
async def test_ocrcore_supported_lang_param():
    img_path = "gran_registro"
    lang = "eng"
    result = await ocr_core(img_path=img_path, lang=lang)
    assert isinstance(result, str), "Should return a string"


@pytest.mark.asyncio
async def test_ocrcore_invalid_lang_param():
    img_path = "gran_registro"
    lang = "ger"
    with pytest.raises(ValueError) as e:
        await ocr_core(img_path=img_path, lang=lang)
    assert (
        str(e.value)
        == f"Language {lang} not supported. Please choose between 'eng' or 'spa'."
    ), "Should raise a ValueError with the correct error message"
