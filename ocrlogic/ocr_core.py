import pytesseract as tesseract
from PIL import Image

from ocrlogic.image_utils import open_static_image


def ocr_core(img_path, lang="eng"):
    """
    This function will handle the core OCR processing of images.

    Parameters:
    img_path (str): The path (or filename) to the image to be processed.
    lang (str): The language to be used for OCR processing.
        Options: "eng" (English) or "spa" (Spanish).

    """
    if lang not in ["eng", "spa"]:
        raise ValueError(f"Language {lang} not supported. Please choose between 'eng' or 'spa'.")

    print(f"Searching for {img_path}")

    # Execution searching in ./static/images directory
    with open_static_image(img_path) as img:
        if img is not None:
            return tesseract.image_to_string(Image.open(img), lang=lang)
