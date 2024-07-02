import os
import shutil
from contextlib import contextmanager

from utils.config import IMG_ROUTES


def _save_file_to_server(uploaded_file, path=".", save_as="default"):
    extension = os.path.splitext(uploaded_file.filename)[-1]
    temp_file = os.path.join(path, save_as + extension)

    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    return temp_file


def _search_img(img_path):
    """
    Search images in the './static/images' directory.
    """
    for img in IMG_ROUTES:
        if img_path in img:
            return img
    return None


@contextmanager
def open_static_image(img_path):
    # Initial configuration: search for the image
    img = _search_img(img_path)
    try:  # self.__enter__
        if img is not None:
            print(f"Found {img_path}")
            # Yield the resource: in this case, the path of the found image
            yield img
        else:
            # If the image is not found, you can either yield None or raise an exception
            yield None
    finally:  # self.__exit__
        pass
