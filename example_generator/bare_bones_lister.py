from bare_bones_word_generator import bare_bones_word_generator


def bare_bones_lister(cell_length, number, height, length):
    return [[[bare_bones_word_generator(cell_length) for j in range(length)] for i in range(height)] for n in range(number)]