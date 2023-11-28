# Nov-27-2023
# create_table.py

import sys
import math
import numpy as np
from numpy import ndarray
from itertools import combinations

from shapes_recognition.src import cfg


def create_table(list_of_peaks) -> (ndarray, int):

    first = list_of_peaks[0]
    y_peaks_0 = first[0]
    x_peaks_0 = first[1]

    if y_peaks_0 != cfg.Y0 or x_peaks_0 != cfg.X0:
        print(f'\nSomething is going wrong')
        sys.exit(1)

    list_of_peaks_half = []
    for item in list_of_peaks:
        if item[0] > cfg.size_roi_half:
            continue
        list_of_peaks_half.append(item)

    list_of_peaks_1 = list_of_peaks_half[1:]

    arr_out = np.array(list(combinations(list_of_peaks_1, 2)))
    n_combinations = arr_out.shape[0]

    table_rows = n_combinations
    table_cols = 4

    table = np.zeros((table_rows, table_cols), dtype=np.int32)

    n_rows: int = 0
    for n in range(table_rows):

        item_1 = arr_out[n, 0]
        item_2 = arr_out[n, 1]

        y1 = item_1[0]
        x1 = item_1[1]

        y2 = item_2[0]
        x2 = item_2[1]

        x_blue, y_blue, x_red, y_red = set_order(x1, y1, x2, y2)

        if x_blue == -1:
            continue

        table[n_rows, 0] = y_blue
        table[n_rows, 1] = x_blue
        table[n_rows, 2] = y_red
        table[n_rows, 3] = x_red

        n_rows += 1

    return table, n_rows


def set_order(x1: int, y1: int, x2: int, y2: int) -> \
        [int, int, int, int]:

    a1 = get_angle_axe_x(x1, y1)
    a2 = get_angle_axe_x(x2, y2)

    da = abs(a1 - a2)

    x_blue = -1
    y_blue = -1
    x_red = -1
    y_red = -1

    if (da >= cfg.angle_min) and (da <= cfg.angle_max):
        if a2 > a1:
            x_blue = x2
            y_blue = y2
            x_red = x1
            y_red = y1
        else:
            x_blue = x1
            y_blue = y1
            x_red = x2
            y_red = y2

    return [x_blue, y_blue, x_red, y_red]


def get_angle_axe_x(x, y) -> float:

    _x1 = float(x - cfg.X0)
    _y1 = float(cfg.Y0 - y)

    _x2 = 1.0
    _y2 = 0.0

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

        if _y1 < 0.0:
            angle_deg = 360.0 - angle_deg
    else:
        angle_deg = 0.0

    return angle_deg
