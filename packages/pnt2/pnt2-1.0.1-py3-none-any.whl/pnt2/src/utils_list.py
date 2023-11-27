# Nov-26-2023
# utils_list.py

from pnt2.src import cfg_pnt2


def save_list_of_peaks_txt(tag, list_of_peaks):

    data_path = cfg_pnt2.dir_debug + '/' + tag + '.txt'

    with open(data_path, 'w') as fp:
        for item in list_of_peaks:
            fp.write(f'{item}\n')


def read_list_of_peaks_txt(tag):

    list_of_peaks = []

    data_path = cfg_pnt2.dir_debug + '/' + tag + '.txt'

    with open(data_path, 'r') as fp:
        for line in fp:

            # remove linebreak from a current item
            item = line[:-1]

            list_of_peaks.append(item)

    return list_of_peaks


def print_list(tag, any_list):
    print(f'\n{tag}')
    n = 0
    for item in any_list:
        print(f'{n}:\t {item}')
        n += 1
