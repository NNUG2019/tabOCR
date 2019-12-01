from random import choice, choices, random
import numpy as np


def word_generator_old(length):
    """

    word_generator is a simple function generating random strings of specified length.

    :param length: Integer. A length of string to be generated.
    :return: Result string.
    """
    word = ''
    i = 0
    while i < length:
        word += choice('1234567890qwertyuiopasdfghjklzxcvbnm')
        i += 1
    return word


def word_generator(min_length, max_length, word_type):
    length = choice(np.arange(min_length, max_length+1, 1))
    word = choices('1234567890qwertyuiopasdfghjklzxcvbnm', k=length)
    return word_type("".join(word))


def number_generator(number_type, round_range):
    return round(number_type(random()*choice([1,10,100,1000])),
                 choice(round_range))