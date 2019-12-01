from random import choice, choices, random
import numpy as np


def bare_bones_word_generator(length):
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