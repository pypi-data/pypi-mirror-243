# Nov-27-2023
# draw_utils.py

import cv2 as cv

from pnt3.src import cfg_pnt3


def draw_peak(any_image, x, y, color, size, thickness):
    start_point = (x - size, y - size)
    end_point = (x + size, y + size)
    cv.rectangle(
        any_image, start_point, end_point,
        color, thickness)


def draw_text(any_image, x, y, text_color, text):

    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    font_color = text_color
    thickness = 1
    cv.putText(
        any_image, text, (x, y),
        font, font_scale, font_color,
        thickness, cv.LINE_AA)


def draw_peak_color(magnitude, x, y, param):

    thickness = -1
    color = cfg_pnt3.black

    if param < 8:
        size = 9 - param

        if param == 0:
            color = cfg_pnt3.nickel
        if param == 1:
            color = cfg_pnt3.cayenne
        if param == 2:
            color = cfg_pnt3.moss
        if param == 3:
            color = cfg_pnt3.ocean
        if param == 4:
            color = cfg_pnt3.magenta
        if param == 5:
            color = cfg_pnt3.blueberry
        if param == 6:
            color = cfg_pnt3.cayenne
        if param == 7:
            color = cfg_pnt3.nickel

        start_point = (x - size, y - size)
        end_point = (x + size, y + size)
        cv.rectangle(
            magnitude, start_point, end_point,
            color, thickness)
    else:
        radius = 3
        cv.circle(
            magnitude, (x, y), radius,
            color, thickness)
