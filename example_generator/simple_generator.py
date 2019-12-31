from save_csv import save_csv
from bare_bones_lister import bare_bones_lister
from simple_imager import simple_imager


def simple_generator(number, path):
    cell_length = 5
    height = 10
    length = 10
    lst = bare_bones_lister(cell_length, number, height, length)
    save_csv(lst, path)
    simple_imager(lst, path)
