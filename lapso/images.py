from PIL import Image
import os


def get_image_properties(file):
    img = Image.open(file)
    return os.stat(file).st_size, img.size[0], img.size[1]
