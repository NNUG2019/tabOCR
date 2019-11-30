from full_imager import full_imager
from full_lister import full_lister
from save_csv import save_csv


def full_generator(number, path, height_range=(20, 20), length_range=(20, 20), cell_range=(5, 5)):
    cell_length = 5
    heights = list(range(height_range[0], height_range[1]+1))
    lengths = list(range(length_range[0], length_range[1]+1))
    cells = list(range(cell_range[0], cell_range[1]+1))
    lst = full_lister(number=number, cells=cells, heights=heights, lengths=lengths)
    save_csv(lst, path)
    full_imager(lst, path)
