import os

import pytesseract as tesseract
from PIL import Image

from ocrlogic.image_utils import open_image


def ocr_core(img_path, lang="eng"):
    """
    This function will handle the core OCR processing of images.

    Parameters:
    img_path (str): The path (or filename) to the image to be processed.
    lang (str): The language to be used for OCR processing.
    """
    print(f"Searching for {img_path}")

    # Execution searching in ./static/images directory
    with open_image(img_path) as img:
        if img is not None:
            return tesseract.image_to_string(Image.open(img), lang=lang)
