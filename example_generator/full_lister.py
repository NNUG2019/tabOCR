from word_generator import word_generator
from random import choice


def full_lister(number, cells, heights, lengths):
    dim_tab = [[choice(heights), choice(lengths)] for i in range(number)]
    return [[[word_generator(length=choice(cells)) for j in range(d[1])]
            for i in range(d[0])] for d in dim_tab]
