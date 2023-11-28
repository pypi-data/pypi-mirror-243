# Nov-27-2023
# create_joint_table.py

import numpy as np
from numpy import ndarray

from pnt3.src import cfg_pnt3
from pnt3.src.get_angle import get_angle


def create_joint_table(
        image_table, n_image_table_rows,
        templ_table, n_templ_table_rows) -> (ndarray, int):

    n_joint_table_rows = n_image_table_rows * n_templ_table_rows

    joint_table = np.zeros((n_joint_table_rows, 8), dtype=np.int32)

    n_rows: int = 0
    for n_image in range(n_image_table_rows):

        y_image_blue = image_table[n_image, 0]
        x_image_blue = image_table[n_image, 1]
        y_image_red = image_table[n_image, 2]
        x_image_red = image_table[n_image, 3]

        angle_image = \
            get_angle(x_image_blue, y_image_blue, x_image_red, y_image_red)

        if angle_image == float(0):
            continue

        for n_templ in range(n_templ_table_rows):

            y_templ_blue = templ_table[n_templ, 0]
            x_templ_blue = templ_table[n_templ, 1]
            y_templ_red = templ_table[n_templ, 2]
            x_templ_red = templ_table[n_templ, 3]

            angle_templ = \
                get_angle(x_templ_blue, y_templ_blue, x_templ_red, y_templ_red)
            
            if angle_templ == float(0):
                continue

            if angle_image > angle_templ:
                angle_ratio = angle_image / angle_templ
            else:
                angle_ratio = angle_templ / angle_image

            if angle_ratio > cfg_pnt3.angle_ratio_threshold:
                continue

            joint_table[n_rows, 0] = y_image_blue
            joint_table[n_rows, 1] = x_image_blue
            joint_table[n_rows, 2] = y_image_red
            joint_table[n_rows, 3] = x_image_red
            joint_table[n_rows, 4] = y_templ_blue
            joint_table[n_rows, 5] = x_templ_blue
            joint_table[n_rows, 6] = y_templ_red
            joint_table[n_rows, 7] = x_templ_red

            n_rows += 1

    return joint_table, n_rows
