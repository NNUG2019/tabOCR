from random import choice, random, randrange
import numpy as np
import yaml
import logging
from os.path import join
from itertools import groupby
from parameters_generator import (generate_words_params, COLUMN_TYPE,
                                  ROUND_RANGE, NUMBER_RANGE, MAX_WORD_LENGTH,
                                  MIN_WORD_LENGTH)

logger = logging.getLogger("logs")


def define_words_list(path=""):
    """ Define a list of possible words to use (out of 3000 most common English
        words).
        :Arguments:
            path: str:: path to the yaml file containing words and their length
        :Returns:
            dict: words grouped by their length:
                  key: int:: word length
                  value: list:: words of specified length
    """
    if path:
        path = join(path, "words_list.yaml")
    else:
        path = "config/words_list.yaml"
    with open(path) as file:
        words_list = yaml.load(file, Loader=yaml.FullLoader)
    d = {}
    words_list = sorted(words_list, key=lambda s: s[1])
    for key, values in groupby(words_list, lambda s: s[1]):
        d = {**d, key: list(map(lambda s: s[0], values))}

    return d


def add_string_header(numbers, words_corpus, words_params):
    """ Add a text header to the column containing numbers.
        :Arguments:
            numbers: list:: list of numbers (column)
            words_corpus: dict:: words grouped by their length
            words_params: randomly generated words parameters
        :Returns:
            list: list of numbers (column) with the first element changed
                  to text
    """
    word_type = words_params['word_type']
    numbers[0] = word_type(choice(
        words_corpus[choice(list(words_corpus.keys()))]))
    return numbers


def generate_words(words_corpus, columns_number, rows_number, columns_type):
    """ Generate table contents for a specific number of rows and columns of
        a specific type (words, numbers, mixed).
        :Arguments:
            words_corpus: dict:: words grouped by their length
            columns_number: int: number of columns
            rows_number: int:: number of rows
            columns_type: str:: columns type, ie. number, string, mixed
        :Returns:
            list of lists: content of the table (each sublist corresponds to
                           one column)
    """
    return [words_generator(words_corpus, rows_number, columns_type)
            for c in range(1, (columns_number+1))]


def words_generator(words_corpus, rows_number, columns_type):
    """ Generate content for column for a specific number of rows of
        a specific type (words or numbers).
        :Arguments:
            words_corpus: dict:: words grouped by their length
            rows_number: int:: number of rows
            columns_type: str:: columns type, ie. number, string, mixed
        :Returns:
            list: content of the column
    """
    words_params = generate_words_params(columns_type)
    if columns_type == "mixed":
        columns_type = choice(COLUMN_TYPE)
    if columns_type == "string":
        return [word_generator(words_corpus, words_params)
                for r in range(1, (rows_number+1))]
    elif columns_type == "number":
        numbers = [number_generator(words_params)
                   for r in range(1, (rows_number+1))]
        if list(filter(lambda x: x > 8, map(lambda x: len(x), numbers))):
            logger.debug("Numbers: {}".format(numbers))
        return add_string_header(numbers, words_corpus, words_params)
    elif columns_type == "mixed":
        mixed = [mixed_generator(words_corpus, words_params)
                 for r in range(1, (rows_number+1))]
        if list(filter(lambda x: x > 8, map(lambda x: len(x), mixed))):
            logger.debug("Mixed: {}".format(mixed))
        return add_string_header(mixed, words_corpus, words_params)
    else:
        raise ValueError("No such type of column {}".format(columns_type))


def word_generator(words_corpus, words_params):
    """ Generate single word of randomly/fixed specified lenght,
        lower/upper/title style, etc. (defined by words parameters) from the
        list of words.
        :Arguments:
            words_corpus: dict:: words grouped by their length
            words_params: dict:: randomly generated words parameters
        :Returns:
            str: single word
    """
    is_change_separator = words_params['is_change_separator']
    word_type = words_params['word_type']
    is_double_word = choice([True, False])
    length = choice(np.arange(words_params['min_length'],
                              words_params['max_length']+1, 1))
    word1 = choice(words_corpus[length])
    free_space = MAX_WORD_LENGTH - length
    if free_space > 3:
        if is_double_word:
            word2 = choice(words_corpus[choice(np.arange(MIN_WORD_LENGTH,
                                                         free_space))])
        else:
            return word_type(word1)
        if is_change_separator:
            return word_type(word1 + choice([" ", ",", "/", "-"]) + word2)
        else:
            return word_type(word1 + " " + word2)
    return word_type(word1)


def number_generator(words_params):
    """ Generate number int/float from the randomly/fixed specified range,
        randomly/fixed specified round number, etc.
        :Arguments:
            words_params: dict:: randomly generated words parameters
        :Returns:
            int: single number (int/float)
    """
    number_type = words_params['number_type']
    length = choice(np.arange(words_params['min_number_length'],
                              words_params['max_number_length']+1, 1))
    number_length = choice(np.arange(1, length+1))
    round_length = choice(np.arange(0, (length-number_length)+1))
    number_range = choice(NUMBER_RANGE[:(number_length+1)])
    round_range = choice(ROUND_RANGE[:(round_length+1)])
    if (number_length == 1) and (round_length == 0):
        return str(int(random()*10))
    else:
        return str(round(number_type(random()*number_range), round_range))


def mixed_generator(words_corpus, words_params):
    """ """
    word_type = words_params['word_type']
    length = choice(np.arange(words_params['min_length'],
                              words_params['max_length']+1, 1))
    sep = words_params['separator']
    free_space = length - len(sep)
    if free_space > 3:
        word_length = choice(np.arange(MIN_WORD_LENGTH, (free_space-1)+1, 1))
        word = choice(words_corpus[word_length])
        free_space -= word_length
        number_range = [10, 100, 1000][:free_space]
        number_range = choice(number_range)
        number = str(randrange(0, number_range))
        word_first = words_params['is_word_first']
        return word_type(word + sep + number) if word_first else word_type(number + sep + word)
    else:
        return word_type(choice(words_corpus[length]))


def mixed_generator2(words_corpus, words_params):
    """ """
    word_type = words_params['word_type']
    length = choice(np.arange(words_params['min_length'],
                              words_params['max_length']+1, 1))
    number_range = [10, 100, 1000][:MAX_WORD_LENGTH - (length-1)]
    number_range = choice(number_range)
    number = str(randrange(0, number_range))
    sep = words_params['separator']
    if length > 3:
        word = choice(words_corpus[length-1])
        word_first = words_params['is_word_first']
        return word + sep + number if word_first else number + sep + word
    else:
        return word_type(choice(words_corpus[length]))
