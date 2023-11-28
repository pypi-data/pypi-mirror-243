# Nov-27-2023
# show_results.py

from shapes_recognition.src.save_results import save_self_study_results, save_recognition_results
from shapes_recognition.src.get_results import get_self_study_results, get_recognition_results


def show_self_study_results(list_self_study_in,
                            list_self_study_out):

    save_self_study_results(list_self_study_in,
                            list_self_study_out)

    get_self_study_results(list_self_study_in,
                           list_self_study_out)


def show_recognition_results(recogn_dictionary):

    save_recognition_results(recogn_dictionary)

    get_recognition_results(recogn_dictionary)
