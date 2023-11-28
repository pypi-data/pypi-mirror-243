# Nov-27-2023
# draw_result.py

import cv2 as cv

from pnt3.src import cfg_pnt3


def draw_result(tag):

    path_in = cfg_pnt3.dir_debug + '/' + tag + '_peaks.png'
    magn_peaks = cv.imread(path_in, cv.IMREAD_UNCHANGED)

    x1: int = 0
    y1: int = 0
    x2: int = 0
    y2: int = 0
    x3: int = cfg_pnt3.X0
    y3: int = cfg_pnt3.Y0

    if tag == 'image':
        x1 = cfg_pnt3.x_image_red
        y1 = cfg_pnt3.y_image_red
        x2 = cfg_pnt3.x_image_blue
        y2 = cfg_pnt3.y_image_blue

    if tag == 'templ':
        x1 = cfg_pnt3.x_templ_red
        y1 = cfg_pnt3.y_templ_red
        x2 = cfg_pnt3.x_templ_blue
        y2 = cfg_pnt3.y_templ_blue

    thickness = 1

    """
    cv.line(magn_peaks,
            (x1, y1),
            (x2, y2),
            cfg_pnt3.clover, thickness)  # green

    cv.line(magn_peaks,
            (x1, y1),
            (x3, y3),
            cfg_pnt3.maraschino, thickness)  # red

    cv.line(magn_peaks,
            (x2, y2),
            (x3, y3),
            cfg_pnt3.aqua, thickness)  # blue
    """

    cv.line(magn_peaks,
            (x1, y1),
            (x2, y2),
            cfg_pnt3.black, thickness)

    cv.line(magn_peaks,
            (x1, y1),
            (x3, y3),
            cfg_pnt3.black, thickness)

    cv.line(magn_peaks,
            (x2, y2),
            (x3, y3),
            cfg_pnt3.black, thickness)

    path_out = cfg_pnt3.dir_debug + '/' + tag + '_result.png'
    cv.imwrite(path_out, magn_peaks)
