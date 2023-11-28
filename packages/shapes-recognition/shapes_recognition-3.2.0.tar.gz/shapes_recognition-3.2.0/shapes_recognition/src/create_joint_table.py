# Nov-27-2023
# create_joint_table.py

import math
import numpy as np
from numpy import ndarray

from shapes_recognition.src import cfg


def create_joint_table(
        image_table, n_image_table_rows,
        templ_table, n_templ_table_rows) -> (ndarray, int):

    n_joint_table_rows = n_image_table_rows * n_templ_table_rows

    joint_table = np.zeros((n_joint_table_rows, 8), dtype=np.int32)

    n_rows: int = 0
    for n_image in range(n_image_table_rows):

        y1_image = image_table[n_image, 0]
        x1_image = image_table[n_image, 1]
        y2_image = image_table[n_image, 2]
        x2_image = image_table[n_image, 3]

        angle_image = \
            get_angle(x1_image, y1_image, x2_image, y2_image)

        if angle_image == float(0):
            continue

        for n_templ in range(n_templ_table_rows):

            y1_templ = templ_table[n_templ, 0]
            x1_templ = templ_table[n_templ, 1]
            y2_templ = templ_table[n_templ, 2]
            x2_templ = templ_table[n_templ, 3]

            angle_templ = \
                get_angle(x1_templ, y1_templ, x2_templ, y2_templ)
            
            if angle_templ == float(0):
                continue

            if angle_image > angle_templ:
                angle_ratio = angle_image / angle_templ
            else:
                angle_ratio = angle_templ / angle_image

            if angle_ratio > cfg.angle_ratio_threshold:
                continue

            joint_table[n_rows, 0] = y1_image
            joint_table[n_rows, 1] = x1_image
            joint_table[n_rows, 2] = y2_image
            joint_table[n_rows, 3] = x2_image
            joint_table[n_rows, 4] = y1_templ
            joint_table[n_rows, 5] = x1_templ
            joint_table[n_rows, 6] = y2_templ
            joint_table[n_rows, 7] = x2_templ

            n_rows += 1

    return joint_table, n_rows


def get_angle(x_a, y_a, x_b, y_b) -> float:

    _x1 = float(x_a - cfg.X0)
    _y1 = float(cfg.Y0 - y_a)

    _x2 = float(x_b - cfg.X0)
    _y2 = float(cfg.Y0 - y_b)

    top = (_x1 * _x2) + (_y1 * _y2)
    bottom = math.sqrt((_x1 * _x1) + (_y1 * _y1)) * math.sqrt((_x2 * _x2) + (_y2 * _y2))

    if bottom > 0.0:
        cos_angle = top / bottom

        if cos_angle > 1.0:
            cos_angle = 1.0
        if cos_angle < -1.0:
            cos_angle = -1.0

        angle_rad = math.acos(cos_angle)
        angle_deg = math.degrees(angle_rad)
    else:
        angle_deg = 0.0

    return angle_deg
