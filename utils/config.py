import os

# Create a list of each of the image files in the static/img directory
img_dir = './static/img'
img_files = os.listdir(img_dir)
IMG_ROUTES = [os.path.join(img_dir, img_file) for img_file in img_files]
