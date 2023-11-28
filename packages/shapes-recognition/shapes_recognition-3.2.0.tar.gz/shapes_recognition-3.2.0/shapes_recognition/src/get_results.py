# Nov-27-2023
# get_results.py

import cv2 as cv

from shapes_recognition.src import cfg
from shapes_recognition.src.create_template import create_template


def get_self_study_results(
        list_self_study_in, list_self_study_out):

    rows = cfg.n_items
    cols = cfg.n_types

    cfg.show_caption = False
    b_img_template, g_img_template, r_img_template = \
        create_template(rows, cols)

    create_self_study_in_table(
        b_img_template, g_img_template, r_img_template,
        list_self_study_in)

    cfg.show_caption = True
    b_img_template, g_img_template, r_img_template = \
        create_template(rows, cols)

    create_self_study_out_table(
        b_img_template, g_img_template, r_img_template,
        list_self_study_out)


def create_self_study_in_table(
        b_img_template, g_img_template, r_img_template,
        list_self_study_in):

    image_table = create_image_table(
                    b_img_template, g_img_template, r_img_template,
                    list_self_study_in)

    path = cfg.dir_results + '/SELF_STUDY_INPUT.png'

    cv.imwrite(path, image_table)


def create_self_study_out_table(
        b_img_template, g_img_template, r_img_template,
        list_self_study_out):

    image_table = create_image_table(
                    b_img_template, g_img_template, r_img_template,
                    list_self_study_out)

    path = cfg.dir_results + '/SELF_STUDY_OUTPUT.png'

    cv.imwrite(path, image_table)


def create_image_table(
        b_img_template, g_img_template, r_img_template,
        list_data):

    n_images = len(list_data)

    b_list_data = []
    g_list_data = []
    r_list_data = []

    for n in range(n_images):

        image_path = list_data[n]

        image = cv.imread(image_path, cv.IMREAD_UNCHANGED)

        if image.ndim == 2:
            image = cv.cvtColor(image, cv.COLOR_GRAY2RGB)

        b_image, g_image, r_image = cv.split(image)

        b_list_data.append(b_image)
        g_list_data.append(g_image)
        r_list_data.append(r_image)

    create_image_table_2(b_img_template, b_list_data)
    create_image_table_2(g_img_template, g_list_data)
    create_image_table_2(r_img_template, r_list_data)

    image_table = cv.merge([b_img_template, g_img_template, r_img_template])

    return image_table


def create_image_table_2(img_template, list_data):

    rows = cfg.n_items
    cols = cfg.n_types

    n_image = 0
    for i in range(cols):

        shift_x = i * cfg.cell_width + (i + 1) * cfg.space

        for j in range(rows):
            shift_y = j * cfg.cell_height + cfg.caption_height + j * cfg.space

            image = list_data[n_image]
            n_image += 1

            add_shape_border(image)

            img_template[
                shift_y:cfg.cell_height + shift_y:,
                shift_x:cfg.cell_width + shift_x:] = image[0::, 0::]


def get_recognition_results(recogn_dictionary):

    rows = cfg.n_items
    cols = cfg.n_types

    cfg.show_caption = True
    b_img_template, g_img_template, r_img_template = create_template(rows, cols)

    create_recognition_table(
        b_img_template, g_img_template, r_img_template,
        recogn_dictionary)


def create_recognition_table(
        b_img_template, g_img_template, r_img_template,
        recogn_dictionary):

    nA = 0
    nB = 0
    nC = 0
    nD = 0

    for key, value in recogn_dictionary.items():

        if value == 'A':
            if nA < cfg.n_items:
                shift_x = 0 * cfg.cell_width + 1 * cfg.space
                nA = create_recognition_table_2(
                            shift_x, key, nA,
                            b_img_template, g_img_template, r_img_template)

        if value == 'B':
            if nB < cfg.n_items:
                shift_x = 1 * cfg.cell_width + 2 * cfg.space
                nB = create_recognition_table_2(
                            shift_x, key, nB,
                            b_img_template, g_img_template, r_img_template)

        if value == 'C':
            if nC < cfg.n_items:
                shift_x = 2 * cfg.cell_width + 3 * cfg.space
                nC = create_recognition_table_2(
                            shift_x, key, nC,
                            b_img_template, g_img_template, r_img_template)

        if value == 'D':
            if nD < cfg.n_items:
                shift_x = 3 * cfg.cell_width + 4 * cfg.space
                nD = create_recognition_table_2(
                            shift_x, key, nD,
                            b_img_template, g_img_template, r_img_template)

    img_template = cv.merge([b_img_template, g_img_template, r_img_template])

    path = cfg.dir_results + '/RECOGNITION.png'

    cv.imwrite(path, img_template)


def create_recognition_table_2(
        shift_x, key, n_column,
        b_img_template, g_img_template, r_img_template):

    shift_y = n_column * cfg.cell_height + cfg.caption_height + n_column * cfg.space
    n_column += 1

    image = cv.imread(key, cv.IMREAD_UNCHANGED)

    if image.ndim == 2:
        image = cv.cvtColor(image, cv.COLOR_GRAY2RGB)

    b_image, g_image, r_image = cv.split(image)

    add_shape_border(b_image)
    add_shape_border(g_image)
    add_shape_border(r_image)

    b_img_template[
        shift_y:cfg.cell_height + shift_y:,
        shift_x:cfg.cell_width + shift_x:] = b_image[0::, 0::]
    g_img_template[
        shift_y:cfg.cell_height + shift_y:,
        shift_x:cfg.cell_width + shift_x:] = g_image[0::, 0::]
    r_img_template[
        shift_y:cfg.cell_height + shift_y:,
        shift_x:cfg.cell_width + shift_x:] = r_image[0::, 0::]

    return n_column


def add_shape_border(image):

    for j in range(cfg.cell_height):
        image[j, 0] = cfg.color_border
        image[j, cfg.cell_width - 1] = cfg.color_border

    for i in range(cfg.cell_width):
        image[0, i] = cfg.color_border
        image[cfg.cell_height - 1, i] = cfg.color_border
