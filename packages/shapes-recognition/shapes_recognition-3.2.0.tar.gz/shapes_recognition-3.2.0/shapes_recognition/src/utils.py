# Nov-27-2023
# utils.py

import sys
from pathlib import Path
import cv2 as cv
import random

from shapes_recognition.src import cfg


def init():

    print(f'\nWait...\n')

    dir_name = cfg.dir_results
    path_dir = Path.cwd() / dir_name

    if path_dir.is_dir():
        for child in path_dir.glob('*'):
            if child.is_file():
                child.unlink()
    else:
        create_directory(dir_name)


def create_directory(dir_name):

    path_dir = Path.cwd() / dir_name

    if not path_dir.is_dir():
        path_dir.mkdir()


def remove_directory(dir_name):

    path_dir = Path.cwd() / dir_name

    if path_dir.is_dir():
        for child in path_dir.glob('*'):
            if child.is_file():
                child.unlink()
        path_dir.rmdir()


def get_self_study_data(dir_name):

    path_dir = Path.cwd() / dir_name

    list_self_study_in = read_data(path_dir)

    random.shuffle(list_self_study_in)

    check_self_study_data(list_self_study_in)

    return list_self_study_in


def get_recognition_data(dir_name):

    path_dir = Path.cwd() / dir_name

    if not path_dir.is_dir():
        sys.exit(0)

    list_recognition_in = read_data(path_dir)

    check_recognition_data(list_recognition_in)

    return list_recognition_in


def read_data(dir_name):

    path_dir = Path.cwd() / dir_name

    list_data = []

    for child in path_dir.glob('*'):
        if child.is_file():

            if child.name.startswith('.'):
                continue

            list_data.append(str(child))

    return list_data


def check_self_study_data(list_self_study_in):

    list_number_of_files_possible = []
    for n in range(2, cfg.n_types_max + 1):
        list_number_of_files_possible.append(n * cfg.n_items)

    length = len(list_self_study_in)

    if length in list_number_of_files_possible:

        for path_image in list_self_study_in:

            image = cv.imread(path_image, cv.IMREAD_UNCHANGED)

            if image.shape[0] != cfg.cell_height or image.shape[1] != cfg.cell_width:
                print(f'\nERROR: ' + path_image + ' - incorrect shape size')
                sys.exit(1)
    else:
        print(f'\nERROR: Incorrect number of shapes in the directory "{cfg.dir_self_study}"')
        sys.exit(1)

    cfg.n_types = length // cfg.n_items


def check_recognition_data(list_recognition_in):

    cfg.n_items_recognition = len(list_recognition_in)

    if cfg.n_items_recognition == 0:
        sys.exit(0)

    for path_image in list_recognition_in:

        image = cv.imread(path_image, cv.IMREAD_UNCHANGED)

        if image.shape[0] != cfg.cell_height or image.shape[1] != cfg.cell_width:
            print(f'\nERROR: ' + path_image + ' - incorrect shape size')
            sys.exit(1)
