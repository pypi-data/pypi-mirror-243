# Nov-27-2023
# to_canonical.py

import cv2 as cv
import numpy as np

from shapes_recognition.src import cfg


def to_canonical(image_gray) -> np.uint8:
    # ---------------------------------------------------------
    image_scale = cv.resize(
        image_gray,
        (cfg.canonical_size, cfg.canonical_size),
        cv.INTER_LANCZOS4)
    # ---------------------------------------------------------
    image_invert = np.invert(image_scale)
    # ---------------------------------------------------------
    image_canonical \
        = np.zeros((cfg.canonical_size, cfg.canonical_size),
                   dtype=np.uint8)
    cv.normalize(image_invert, image_canonical, 0, 255, cv.NORM_MINMAX)
    # ---------------------------------------------------------
    return np.uint8(image_canonical)
