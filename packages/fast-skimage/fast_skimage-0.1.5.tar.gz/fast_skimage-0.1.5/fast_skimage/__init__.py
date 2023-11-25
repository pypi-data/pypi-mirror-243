import os
from fast_skimage.Image import Image

# Get the directory where the package is installed
PACKAGE_DIR = os.path.dirname(__file__)

def get_image_path(filename):
    return os.path.join(PACKAGE_DIR, 'Pictures', filename)


def zebra():
    return Image('Pictures/zebra.jpg')

def noisy_astronaut():
    return Image('Pictures/astronaut_noisy.jpg')

def new_york():
    return Image('Pictures/nyc.jpg')

def beach():
    return Image('Pictures/etretat.jpg')

def camera():
    return Image('Pictures/camera.jpg')

def walking():
    return Image('Pictures/walking.jpg')

def watermark_ULB():
    return Image('Pictures/watermark.png')
