from random import choice, random
import numpy as np
import yaml
from os.path import join
from itertools import groupby
from parameters_generator import generate_words_params, COLUMN_TYPE


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
        return add_string_header(numbers, words_corpus, words_params)
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
    word_type = words_params['word_type']
    length = choice(np.arange(words_params['min_length'],
                              words_params['max_length']+1, 1))
    word = choice(words_corpus[length])
    return word_type(word)


def number_generator(words_params):
    """ Generate number int/float from the randomly/fixed specified range,
        randomly/fixed specified round number, etc.
        :Arguments:
            words_params: dict:: randomly generated words parameters
        :Returns:
            int: single number (int/float)
    """
    number_type = words_params['number_type']
    return str(round(number_type(random()*choice([1, 10, 100, 1000])),
                     choice(words_params['round_range'])))
