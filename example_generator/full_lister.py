from word_generator import word_generator
from parameters_generator import generate_data_set_params
from random import choice


def full_lister(number, cells):
    """

    full_lister generates random data sets for files to be used in other functions.

    :param number: Integer. Number of file data sets to be generated.
    :param cells: Iterable containing allowed values for character strings in cells.
    :param heights: Iterable containing allowed values for row number interpreted as in full_imager.
    :param lengths: Iterable containing allowed values for column number interpreted as in full_imager.
    :return: Three dimensional list of strings containing data for files in format lst[file][column][row].
    """

    parameters = [generate_data_set_params() for i in range(number)]
    return [[[word_generator(length=choice(cells)) for j in range(d["rows_number"])]
            for i in range(d["columns_number"])] for d in parameters]
