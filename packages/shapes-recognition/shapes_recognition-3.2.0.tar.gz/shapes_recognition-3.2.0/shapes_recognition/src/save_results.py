# Nov-27-2023
# save_results.py

from datetime import datetime

from shapes_recognition.src import cfg


def save_self_study_results(list_self_study_in,
                            list_self_study_out):

    path = cfg.dir_results + '/self_study.txt'

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    with open(path, 'w') as f:

        f.write(dt_string)
        f.write('\n\nSELF-STUDY INPUT:\n')
        n = 0
        for item in list_self_study_in:
            line = str(n) + ':\t' + item
            f.write(line + '\n')
            n += 1

        f.write('\nSELF-STUDY OUTPUT:\n')
        n = 0
        for item in list_self_study_out:
            line = str(n) + ':\t' + item
            f.write(line + '\n')
            n += 1

        f.write('\nn_types = ' + str(cfg.n_types) + '\t\t' +
                'n_items = ' + str(cfg.n_items) + '\n\n' +
                'self-study time = ' + cfg.time_self_study + '\n')


def save_recognition_results(recogn_dictionary):

    path = cfg.dir_results + '/recognition.txt'

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    with open(path, 'w') as f:

        f.write(dt_string)
        f.write('\n\nRECOGNITION:\n')

        n = 0
        for key, value in recogn_dictionary.items():
            line = str(n) + ':\t' + key + '  :  ' + value
            f.write(line + '\n')
            n += 1

        f.write('\nn_types = ' + str(cfg.n_types) + '\t\t' +
                'n_items = ' + str(cfg.n_items) + '\t\t' +
                'n_items_recognition = ' + str(cfg.n_items_recognition) + '\n\n' +
                'recognition time = ' + cfg.time_recognition + '\n')
