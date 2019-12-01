from random import choice, choices, random
import numpy as np
from parameters_generator import generate_word_params


def word_generator(length):
    """
    word_generator is a simple function generating random strings of specified length.
    :param length: Integer. A length of string to be generated.
    :return: Result string.
    """
    parameters = generate_word_params()
    if parameters["column_type"]=="number":
        return number_generator(number_type=parameters["number_type"], round_range=parameters["round_range"])
    return string_generator(min_length=parameters["min_length"], max_length=parameters["max_length"],
                            word_type=parameters["word_type"])


def string_generator(min_length, max_length, word_type):
    length = choice(np.arange(min_length, max_length+1, 1))
    word = choices('1234567890qwertyuiopasdfghjklzxcvbnm', k=length)
    return word_type("".join(word))


def number_generator(number_type, round_range):
    return str(round(number_type(random()*choice([1, 10, 100, 1000])), choice(round_range)))