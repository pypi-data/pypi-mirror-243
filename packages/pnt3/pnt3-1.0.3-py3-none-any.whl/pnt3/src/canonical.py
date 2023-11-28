# Nov-27-2023
# canonical.py

import cv2 as cv
import numpy as np

from pnt3.src import cfg_pnt3


def convert_to_canonical(tag: str, path: str) -> np.uint8:
    # ---------------------------------------------------------
    if tag == 'image':
        cfg_pnt3.path_image = path
    if tag == 'templ':
        cfg_pnt3.path_templ = path
    # ---------------------------------------------------------
    image_gray = cv.imread(path, cv.IMREAD_GRAYSCALE)

    image_canonical = to_canonical(image_gray)
    # ---------------------------------------------------------
    return image_canonical


def to_canonical(image_gray) -> np.uint8:
    # ---------------------------------------------------------
    width = image_gray.shape[1]
    height = image_gray.shape[0]

    max_original_size = max(height, width)
    if max_original_size > cfg_pnt3.canonical_size:
        scale = float(cfg_pnt3.canonical_size) / float(max_original_size)
        width: int = int(width * scale)
        height: int = int(height * scale)
        dim = (width, height)
        image_scale = cv.resize(image_gray, dim, cv.INTER_LANCZOS4)
        image_invert = np.invert(image_scale)
    else:
        image_invert = np.invert(image_gray)
    # ---------------------------------------------------------
    image_canonical = np.zeros((height, width), dtype=np.uint8)
    cv.normalize(image_invert, image_canonical, 0, 255, cv.NORM_MINMAX)
    # ---------------------------------------------------------
    return np.uint8(image_canonical)
