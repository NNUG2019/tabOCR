from save_csv import save_csv
from bare_bones_lister import bare_bones_lister
from bare_bones_imager import bare_bones_imager


def bare_bones_generator(number, path):
    cell_length = 5
    height = 20
    length = 10
    lst = bare_bones_lister(cell_length, number, height, length)
    save_csv(lst, path)
    bare_bones_imager(lst, path)
