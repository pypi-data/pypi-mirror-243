# Nov-27-2023
# get_column_data.py

import cv2 as cv
import numpy as np

from shapes_recognition.src import cfg
from shapes_recognition.src.to_canonical import to_canonical


def get_column_data(list_in):

    column_data_width = cfg.canonical_size
    column_data_height = cfg.canonical_size * len(list_in)

    column_data = \
        np.zeros((column_data_height, column_data_width), dtype=np.uint8)

    n_row: int = 0
    for path in list_in:

        image_gray = cv.imread(path, cv.IMREAD_GRAYSCALE)

        image_canonical = to_canonical(image_gray)

        shift_vert = n_row * cfg.canonical_size

        column_data[
            shift_vert:shift_vert + cfg.canonical_size:,
            0:cfg.canonical_size:] = image_canonical[0::, 0::]

        n_row += 1

    return column_data
