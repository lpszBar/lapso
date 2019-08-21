from PIL import Image
from PIL.ExifTags import TAGS
import os


def get_image_properties(file):
    img = Image.open(file)
    try:
        exif = {TAGS[k]: v for k, v in img._getexif().items()
                if k in TAGS}
    except AttributeError as e:
        exif = {}
        print("Date not found. Ignoring.")
    return os.stat(file).st_size, img.size[0], img.size[1], exif
