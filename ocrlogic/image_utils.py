from contextlib import contextmanager

from utils.config import IMG_ROUTES


def search_img(img_path):
    """
    Search images in the './static/images' directory.
    """
    for img in IMG_ROUTES:
        if img_path in img:
            return img
    return None


@contextmanager
def open_image(img_path):
    # Initial configuration: search for the image
    img = search_img(img_path)
    try: #self.__enter__
        if img is not None:
            print(f"Found {img_path}")
            # Yield the resource: in this case, the path of the found image
            yield img
        else:
            # If the image is not found, you can either yield None or raise an exception
            yield None
    finally: # self.__exit__
        pass

