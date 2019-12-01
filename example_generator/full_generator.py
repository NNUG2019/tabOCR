from full_imager import full_imager
from full_lister import full_lister
from save_csv import save_csv


def full_generator(number, path, height_range=(20, 20), length_range=(20, 20), cell_range=(5, 5)):
    """

    full_generator is a sort of interface for other functions.

    :param number: Integer. Number of data sets to be generated.
    :param path: Path for to the directory where files should be saved.
    :param height_range: Iterable of dimensions [2] containing two integers representing allowed range for row number
    interpreted as in full_imager.
    :param length_range: Iterable of dimensions [2] containing two integers representing allowed range for column number
    interpreted as in full_imager.
    :param cell_range: Iterable of dimensions [2] containing two integers representing allowed range for sting lengths
    in cells.
    :return:
    """

    cells = list(range(cell_range[0], cell_range[1]+1))
    lst = full_lister(number=number, cells=cells)
    save_csv(lst, path)
    full_imager(lst, path)
