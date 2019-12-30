import numpy as np
from random import choice
import logging

logger = logging.getLogger("logs")

MIN_COLUMNS_NUMBER = 2
MAX_COLUMNS_NUMBER = 5
MIN_ROWS_NUMBER = 2
MAX_ROWS_NUMBER = 10
MIN_FONT_SIZE = 9
MAX_FONT_SIZE = 18
COLUMNS_NUMBER = np.arange(MIN_COLUMNS_NUMBER, MAX_COLUMNS_NUMBER+1, 1)
ROWS_NUMBER = np.arange(MIN_ROWS_NUMBER, MAX_ROWS_NUMBER+1, 1)
FONT_SIZE = np.arange(MIN_FONT_SIZE, MAX_FONT_SIZE+1, 1)
ROUND_RANGE = [0, 1, 2, 3, 4, 5]
NUMBER_RANGE = [1, 10, 100, 1000, 10000, 100000, 1000000]
COLUMNS_TYPE = ["string", "number", "mixed"]
FONT_NAME = ["Arial", "Book Antiqua", "Calibri", "Cambria",
             "Garamond", "Georgia", "Helvetica", "Times New Roman"]
LINE_STYLE = ['medium', 'thick', 'thin', 'double']
LINE_STYLE_HEADER = ['double', 'medium', 'thick', 'thin',
                     'dashed', 'mediumDashed']
HORIZONTAL_ALIGNMENT = ["right", "left", "center"]
VERTICAL_ALIGNMENT = ["bottom", "center", "top"]
IS_BORDER = [True, False]
IS_PARTIAL_BORDER = [True, False]
IS_DIFFERENT_HEADER = [True, False]
IS_COLUMNS_WIDTH_FIXED = [True, False]
WORD_TYPE = [str.lower, str.upper, str.title]
NUMBER_TYPE = [int, float]
COLUMN_TYPE = ["string", "number", "mixed"]
IS_CONTENT_FIXED = [True, False]
COLORS = ["FF0000", "00FF00", "0000FF", "FFFF00", "00FFFF",
          "FF00FF", "008080", "808080", "800000", "008000"]

COLORS_FAMILY = {'yellow': ['f1c232', 'ff3599', 'fff2cc', 'ffffff'],
                 'blue': ['6d9ebb', 'a4c2f4', 'c9daf8', 'ffffff'],
                 'green': ['93c47d', 'b6d7a8', 'd9ead3', 'ffffff'],
                 'cyan': ['76a5af', 'a2c4c9', 'd0e0e3', 'ffffff'],
                 'red': ['e06666', 'ea9999', 'f4cccc', 'ffffff'],
                 'orange': ['f6b26b', 'f9cv9c', 'fce5cd', 'ffffff'],
                 'gray': ['cccccc', 'd9d9d9', 'efefef', 'ffffff']}


PIXEL_COLUMN = 7
PIXEL_ROW = 4/3
FONT_SIZE_WIDTH = 0.5
ONE_LETTER_WIDTH = 3

MIN_WORD_LENGTH = 3
MAX_WORD_LENGTH = 8

# TODO - parametrize MAX_COLUMNS_WIDTH, MAX_ROW_HEIGHT and MAX_COLUMN_WIDTH
# according to the font size and max word length
# MAX_COLUMNS_WIDTH = (round(define_min_column_width(MAX_FONT_SIZE, MAX_WORD_LENGTH)) + 3)*COLUMNS_NUMBER # noqa
MAX_COLUMNS_WIDTH = 155
MIN_COLUMN_WIDTH = 7
MAX_COLUMN_WIDTH = 50
MIN_ROW_HEIGHT = 30
MAX_ROW_HEIGHT = 50
# TODO - parametrize according to the MAX_COLUMNS_WIDTH and columns number
IMG_SHAPE = (740, 1100)
IMG_COL_SHAPE = (740, PIXEL_COLUMN*(
    MAX_COLUMN_WIDTH + int(MAX_COLUMNS_WIDTH/MAX_COLUMNS_NUMBER)))
IMG_ROW_SHAPE = (int(PIXEL_ROW*MAX_ROW_HEIGHT), IMG_COL_SHAPE[1])


def generate_table_params():
    """ Randomly generate table parameters such as columns number, rows number,
        font size, border style, etc.
        :Arguments:
            None
        :Returns:
            dict: table parameters
    """
    return {"columns_number": choice(COLUMNS_NUMBER),
            "rows_number": choice(ROWS_NUMBER),
            "columns_type": choice(COLUMNS_TYPE),
            "is_columns_width_fixed": choice(IS_COLUMNS_WIDTH_FIXED),
            "font_size": choice(FONT_SIZE),
            "font_name": choice(FONT_NAME),
            "line_style": choice(LINE_STYLE),
            "is_different_header": choice(IS_DIFFERENT_HEADER),
            "is_border": choice(IS_BORDER),
            "is_partial_border": choice(IS_PARTIAL_BORDER),
            "horizontal_alingment": choice(HORIZONTAL_ALIGNMENT),
            "vertical_alingment": choice(VERTICAL_ALIGNMENT)}


def generate_header_params():
    """ Randomly generate header parameters such as border style,
        font size, etc.
        :Arguments:
            None
        :Returns:
            dict: table parameters
    """
    line_style = choice(LINE_STYLE_HEADER)
    font_size = choice(FONT_SIZE)
    font_style = {"font_bold": choice([True, False]),
                  "font_italic": choice([True, False])}
    word_type = choice(WORD_TYPE + [lambda s: s])
    return {"line_style": line_style,
            "font_size": font_size,
            "word_type": word_type,
            **font_style}


def generate_words_params(column_type):
    """ Randomly generate parameters of the table content, such as range of
        words length, number type (int/float), etc.
        :Arguments:
            column_type:: str: type of the column, ie. string or number
        :Returns:
            dict: content parameters
    """
    if choice(IS_CONTENT_FIXED):
        min_length = max_length = choice(np.arange(MIN_WORD_LENGTH,
                                                   MAX_WORD_LENGTH+1, 1))
        min_number_length = max_number_length = choice(np.arange(1,
                                                       MAX_WORD_LENGTH+1, 1))
    else:
        min_length = MIN_WORD_LENGTH
        max_length = MAX_WORD_LENGTH
        min_number_length = 1
        max_number_length = MAX_WORD_LENGTH

    return {
        "column_type": column_type if column_type in ["string", "number"]
        else choice(COLUMN_TYPE),
        "word_type": choice(WORD_TYPE),
        "number_type": choice(NUMBER_TYPE),
        "min_length": min_length,
        "max_length": max_length,
        "min_number_length": min_number_length,
        "max_number_length": max_number_length,
        "separator": choice(["_", "-", " - ", "/", ",", ", ", " ", ""]),
        'is_word_first': choice([True, False]),
        'is_change_separator': choice([True, False])
    }


def generate_rows_height(font_size):
    """ Generate row height based on the font size.
        :Arguments:
            font_size:: int: font size
        :Returns:
            int: row height
    """
    min_row_height = MIN_ROW_HEIGHT + 2*(font_size-FONT_SIZE[0])
    row_height = np.arange(MIN_ROW_HEIGHT, MAX_ROW_HEIGHT+1, 1)
    row_height = row_height[row_height >= min_row_height]
    return choice(row_height)


def generate_columns_width(words_list, table_params):
    """ Generate column widths based on the maximum word length in each column
        and the generated table parameters.
        :Arguments:
            words_list:: list of lists: content of each column
            table_params:: dict: randomly generated table parameters
        :Returns:
            list: column widths
    """
    max_words_length = [max(list(map(lambda w: len(w), col_words)))
                        for col_words in words_list]
    minimum_column_widths = [define_min_column_width(table_params['font_size'],
                                                     word_length)
                             for word_length in max_words_length]
    if table_params['is_columns_width_fixed']:
        return generate_fixed_column_width(minimum_column_widths)
    else:
        return generate_variable_column_width(minimum_column_widths,
                                              max_words_length, table_params)


def define_min_column_width(font_size, max_word_length):
    """ Generate mimimum column width based on the words length and font size.
        :Arguments:
            font_size:: int: font size
            max_word_length:: int: the length of the longest word in the column
        :Returns:
            int: minimum column width
    """
    return 1 + MIN_COLUMN_WIDTH +\
        FONT_SIZE_WIDTH * (font_size - FONT_SIZE[0]) +\
        ONE_LETTER_WIDTH * (max_word_length - MIN_WORD_LENGTH)


def generate_fixed_column_width(minimum_column_widths):
    """ Generate equal column widths from the range defined as follows:
        - minimum column width generated by define_min_column_width,
        - maximum column width defined as fixed (global variable).
        :Arguments:
            minimum_column_widths:: list: minimum column widths
        :Returns:
            list: column widths (equal)
    """
    max_column_width = int(MAX_COLUMNS_WIDTH/len(minimum_column_widths))
    if max_column_width > MAX_COLUMN_WIDTH:
        width = choice(np.arange(max(minimum_column_widths),
                                 MAX_COLUMN_WIDTH+1, 1))
    else:
        try:
            width = choice(np.arange(max(minimum_column_widths),
                           max_column_width+1, 1))
        except IndexError:
            logger.error("Wrong columns width; max_column_width: {}, "
                         "minimum_column_widths: {}".
                         format(max_column_width, minimum_column_widths))
            raise
    return [width for c in range(len(minimum_column_widths))]


def generate_variable_column_width(minimum_column_widths, max_words_length,
                                   table_params):
    """ Generate variable column widths. Each column width is generated from
        the range (minimum column width, maximum column width). The maximum
        column width is defined differently depending on the amount of space
        already occupied by the other columns. At the beginning, the minimum
        amount of space needed to place all columns is reserved (equals to
        minimum_column_widths). Thus, the maximum column width can be equal to:
        - if remaining free space is less than minimum column width:
            column width is set to the minimum column width (is not generated)
        - else:
            - the sum of the fixed MAX_COLUMN_WIDTH and minimum column width,
            - the sum of the fixed MAX_COLUMN_WIDTH and remaining free space.
        :Arguments:
            minimum_column_widths:: list: minimum column widths
            max_word_length:: int: the length of the longest word in the column
            table_params:: dict: randomly generated table parameters
        :Returns:
            list: column widths (variable)
    """
    free_columns_space = MAX_COLUMNS_WIDTH - sum(minimum_column_widths)
    width = free_columns_space
    columns_width = []
    for min_col_width in minimum_column_widths:
        if free_columns_space < min_col_width:
            width = min_col_width
        else:
            if free_columns_space > (MAX_COLUMN_WIDTH):
                width = np.arange(min_col_width,
                                  (MAX_COLUMN_WIDTH + min_col_width)+1, 1)
                width = choice(width)
                free_columns_space -= width
            else:
                width = np.arange(min_col_width,
                                  (free_columns_space + min_col_width)+1, 1)
                width = choice(width)
                free_columns_space -= width
        columns_width.append(width)
    return columns_width
