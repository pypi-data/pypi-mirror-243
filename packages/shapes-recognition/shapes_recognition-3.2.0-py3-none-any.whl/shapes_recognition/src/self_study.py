# Nov-27-2023
# self_study.py

import numpy as np
import random
import time
from itertools import combinations
from tqdm import tqdm

import pnt2
import pnt3

from shapes_recognition.src import cfg
from shapes_recognition.src.get_column_data import get_column_data


def self_study(list_self_study_in):

    time1 = time.time()

    random.shuffle(list_self_study_in)

    sl_in_data = get_column_data(list_self_study_in)

    n_shapes: int = cfg.n_types * cfg.n_items

    arr_shapes = np.arange(n_shapes)

    arr_comb = np.array(list(combinations(arr_shapes, cfg.n_items)))

    n_combinations = arr_comb.shape[0]

    arr_similarity = np.zeros((n_shapes, n_shapes), dtype=np.float64)

    shape_i = np.zeros((cfg.canonical_size, cfg.canonical_size), dtype=np.uint8)
    shape_j = np.zeros((cfg.canonical_size, cfg.canonical_size), dtype=np.uint8)

    for i in tqdm(range(n_shapes-1), desc=' self-study'):

        path_i = list_self_study_in[i]

        shift_vert_i = i * cfg.canonical_size

        shape_i[0::, 0::] = sl_in_data[
                                shift_vert_i:shift_vert_i + cfg.canonical_size:,
                                0:cfg.canonical_size:]

        for j in range(i+1, n_shapes):

            path_j = list_self_study_in[j]

            shift_vert_j = j * cfg.canonical_size

            shape_j[0::, 0::] = sl_in_data[
                                    shift_vert_j:shift_vert_j + cfg.canonical_size:,
                                    0:cfg.canonical_size:]

            cfg.path_image = path_i
            cfg.path_templ = path_j

            match cfg.method:

                case 2:
                    arr_similarity[i, j] = pnt2.calc_similarity(np.uint8(shape_i), np.uint8(shape_j))

                case 3:
                    arr_similarity[i, j] = pnt3.calc_similarity(np.uint8(shape_i), np.uint8(shape_j))

                case _:
                    # returns a random floating number between 0 and 1
                    arr_similarity[i, j] = random.random()

    arr_items = np.zeros(cfg.n_items, dtype=np.int32)

    arr_comb_similar = np.zeros(n_combinations, dtype=np.float64)

    for n in range(n_combinations):

        arr_items[:] = arr_comb[n, :]

        val = 0.0
        for i in range(cfg.n_items - 1):
            for j in range(i + 1, cfg.n_items):
                val = val + arr_similarity[arr_items[i], arr_items[j]]

        arr_comb_similar[n] = val

    arr_order = np.arange(n_combinations)

    shell_sort(arr_comb_similar, arr_order, n_combinations)

    arr_comb_order = np.zeros((n_combinations, cfg.n_items), dtype=np.int32)

    for n in range(n_combinations):

        m = arr_order[n]

        for k in range(cfg.n_items):

            arr_comb_order[n, k] = arr_comb[m, k]

    arr_col = np.zeros(cfg.n_items, dtype=np.int32)
    arr_accum = np.empty(n_shapes, dtype=np.int32)
    arr_accum.fill(-1)

    n_copies: int = 0
    for n in range(n_combinations):

        arr_col[:] = arr_comb_order[n, :]

        result = common_member(arr_col, arr_accum)

        if result == 0:

            arr_accum[n_copies * cfg.n_items:(n_copies + 1) * cfg.n_items:] = \
                arr_col[:]

            n_copies += 1

        if n_copies == cfg.n_types:
            break

    list_self_study_out = []
    for n in range(n_shapes):
        m = arr_accum[n]
        image_path = list_self_study_in[m]
        list_self_study_out.append(image_path)

    time2 = time.time()
    m, s = divmod(int(time2 - time1), 60)
    cfg.time_self_study = f'{m:02d} min  {s:02d} sec'

    return list_self_study_out


def shell_sort(vect1, vect2, n):

    gap = n // 2

    while gap > 0:

        for i in range(gap, n):

            j = i - gap

            while j >= 0 and vect1[j] < vect1[j + gap]:
                temp = vect1[j]
                vect1[j] = vect1[j + gap]
                vect1[j + gap] = temp

                temp = vect2[j]
                vect2[j] = vect2[j + gap]
                vect2[j + gap] = temp

                j = j - gap

        gap = gap // 2


def common_member(arr_1, arr_2):

    a_set = set(arr_1)
    b_set = set(arr_2)

    if a_set & b_set:
        return 1
    else:
        return 0
