# Nov-27-2023
# draw_canonical.py

import cv2 as cv
from pathlib import Path

from pnt3.src import cfg_pnt3


def draw_canonical(image, templ):

    canon_image_name = 'canon_' + cfg_pnt3.image_name
    canon_templ_name = 'canon_' + cfg_pnt3.templ_name

    path_image_canon = str(Path.cwd() / cfg_pnt3.dir_debug / canon_image_name)
    path_templ_canon = str(Path.cwd() / cfg_pnt3.dir_debug / canon_templ_name)

    cv.imwrite(path_image_canon, image)
    cv.imwrite(path_templ_canon, templ)
