import numpy as np
from openpyxl.styles import Border, Side
from openpyxl import Workbook
from random import choice, choices, randint, random

COLUMNS_NUMBER = np.arange(2,11,1)
ROWS_NUMBER = np.arange(2,39,1)
COLUMNS_TYPE = ["string", "number", "mixed"]
FONT_SIZE = np.arange(9,19,1)
PIXEL = 7
FONT_NAME = ["Arial", "Book Antiqua", "Calibri", "Cambria",
             "Garamond", "Georgia", "Helvetica", "Times New Roman"]
LINE_STYLE = ['medium', 'thick', 'thin']
LINE_STYLE_HEADER = ['double', 'medium', 'thick', 'thin', 'dashed', 'mediumDashed']
IS_BORDER = [True, False]
IS_PARTIAL_BORDER = [True, False]
IS_DIFFERENT_HEADER = [True, False]

WORD_TYPE = [str.lower, str.upper, str.title]
NUMBER_TYPE = [int, float]
COLUMN_TYPE = ["string", "number"]
IS_CONTENT_FIXED = [True, False]
MIN_COLUMN_WIDTH = 7
MAX_COLUMN_WIDTH = 31
MIN_ROW_HEIGHT = 4
MAX_ROW_HEIGHT = 8
MIN_WORD_LENGTH = 3
MAX_WORD_LENGTH = 8
FONT_SIZE_WIDTH = 1
ONE_LETTER_WIDTH = 3
IMG_SHAPE = (2200, 2200)


def generate_table_params():
    return {"columns_number": choice(COLUMNS_NUMBER), 
            "rows_number": choice(ROWS_NUMBER),
            "columns_type": choice(COLUMNS_TYPE),
            "font_size": choice(FONT_SIZE),
            "font_name": choice(FONT_NAME),
            "line_style": choice(LINE_STYLE),
            "is_different_header": choice(IS_DIFFERENT_HEADER),
            "is_border": choice(IS_BORDER),
            "is_partial_border": choice(IS_PARTIAL_BORDER)}
    

def generate_header_params():
    line_style = choice(LINE_STYLE_HEADER)
    font_size = choice(FONT_SIZE)
    font_style = {"font_bold": choice([True, False]),
                  "font_italic": choice([True, False])}
    return {"line_style": line_style,
            "font_size":font_size,
            **font_style}
    
    
def generate_border(line_style, is_border=False, is_partial_border=False):
    def define_border(style, color):
        return Side(border_style=style, color=color)
    def define_border_style(line_style, color="FFFFFF"):
        return {"top": define_border(line_style, color),
                 "bottom": define_border(line_style, color),
                 "left": define_border(line_style, color),
                 "right": define_border(line_style, color)}
    if is_border:
        style = define_border_style(line_style, color="000000")
        if is_partial_border:
            side = choice(["top", "left"])
            style = define_border_style(line_style)
            style = {**style, side: define_border(line_style, color="000000")}
        return Border(**style)
    else:
        style = define_border_style(line_style)
        return Border(**style)


def generate_row_params(font_size):
    min_row_height = MIN_ROW_HEIGHT + 0.2*(font_size-FONT_SIZE[0])
    row_height = np.arange(MIN_ROW_HEIGHT, MAX_ROW_HEIGHT+1, 1)
    row_height = row_height[row_height>=min_row_height]
    return {"row_height": choice(row_height)}


def generate_column_params(column_type):
    if choice(IS_CONTENT_FIXED):
        min_length = max_length = choice(np.arange(MIN_WORD_LENGTH, MAX_WORD_LENGTH, 1))
        round_range = [choice([0,1,2,3,4])]
    else:
        min_length = MIN_WORD_LENGTH
        max_length = MAX_WORD_LENGTH
        round_range = [0,1,2,3,4]
        
    column_params = {"column_type": choice(COLUMN_TYPE),
                     "word_type": choice(WORD_TYPE),
                     "number_type": choice(NUMBER_TYPE),
                     "min_length": min_length,
                     "max_length": max_length,
                     "round_range": round_range}
    if column_type == "string" or column_type == "number":
        return {**column_params, "column_type": column_type}
    else:
        return column_params


def generate_column_width(font_size, word_max_length):
    min_column_width = MIN_COLUMN_WIDTH + FONT_SIZE_WIDTH*(font_size-FONT_SIZE[0]) + ONE_LETTER_WIDTH*(word_max_length-MIN_WORD_LENGTH)
    max_column_width = MAX_COLUMN_WIDTH
    print(min_column_width, max_column_width)
    column_width = np.arange(min_column_width, max_column_width+1, 1)
    return {"column_width": choice(column_width)}


def generate_blank_col_row_params(rows_number, row_height,
                                  columns_width):
    blank_row_height = IMG_SHAPE[0] - rows_number*row_height*PIXEL
    blank_col_width = IMG_SHAPE[1] - columns_width*PIXEL
    return blank_row_height, blank_col_width