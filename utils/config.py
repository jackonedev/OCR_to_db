import os


# current file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# previous directory from the current file path
ROOT_DIR = os.path.dirname(BASE_DIR)

# Obtain the relative path to the static directory from the current file
STATIC_DIR = os.path.join(ROOT_DIR, "static")

# Create a list of each of the image files in the static/img directory
img_dir = f"{STATIC_DIR}/img"
img_files = os.listdir(img_dir)
IMG_ROUTES = [os.path.join(img_dir, img_file) for img_file in img_files]
