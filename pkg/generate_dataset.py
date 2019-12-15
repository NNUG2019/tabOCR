from excel2img import export_img
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from os.path import join, exists
from os import mkdir
from os import remove
from copy import copy
import json
from skimage.io import imread, imsave
from skimage.color import rgb2gray
import numpy as np
from parameters_generator import (generate_table_params, COLORS, IMG_SHAPE,
                                  generate_header_params, generate_rows_height,
                                  generate_columns_width, IMG_COL_SHAPE)
from style_generator import (generate_border, generate_font,
                             generate_alingment, generate_pattern_fill)
from word_generator import generate_words, define_words_list
import multiprocessing as mp


def convert_to_numeric(words_list):
    """ Convert numbers stored as text to number type (to avoid warning
        in Excel).
        :Arguments:
            words_list: list:: column content
        :Returns:
            list: column content (numbers stored as text converted to numbers)
    """
    if all(map(lambda s: s.isdigit(), words_list)):
        return [words_list[0]] + list(map(int, words_list[1:]))
    else:
        try:
            return [words_list[0]] + list(map(float, words_list[1:]))
        except ValueError:
            return words_list


def generate_table(words_list, table_params, font, border, alignment,
                   rows_height, column_widths):
    """ Generate .xlsx table.
        :Arguments:
            words_list: list of lists:: table content
            table_params: dict:: randomly generated table parameters
            font: Font: Font object
            border: Border:: border object
            alignment: Alignment:: alignment object
            rows_height: int:: row height
            column_widths: list:: column widths
        :Returns:
            workbook: table
    """
    workbook = Workbook()
    sheet = workbook.active
    for c in range(table_params['columns_number']):
        words = convert_to_numeric(words_list[c])
        for r in range(table_params['rows_number']):
            cell = sheet.cell(r+1, c+1)
            cell.value = words[r]
            cell.border = border
            cell.font = font
            cell.alignment = alignment
            sheet.row_dimensions[r+1].height = rows_height
            sheet.column_dimensions[get_column_letter(c+1)].width =\
                column_widths[c]
    if table_params['is_different_header']:
        header_params = generate_header_params()
        word_type = header_params['word_type']
        border = generate_border(header_params['line_style'],
                                 table_params['is_border'],
                                 table_params['is_partial_border'])
        font_header = generate_font(table_params['font_name'],
                                    header_params['font_size'],
                                    header_params['font_bold'],
                                    header_params['font_italic'])
        for c in range(table_params['columns_number']):
            cell = sheet.cell(1, c+1)
            cell.border = border
            cell.font = font_header
            cell.value = word_type(cell.value)

    return workbook


def generate_masks(columns_number, rows_number, column_widths, rows_height):
    """ Generate rgb mask for columns.
        :Arguments:
            columns_number: int:: columns number
            rows_number: int:: rows number
            column_widths: list:: column widths
            rows_height: int:: row height
        :Returns:
            workbook: table (mask)
    """
    workbook = Workbook()
    sheet = workbook.active
    for c in range(columns_number):
        for r in range(rows_number):
            cell = sheet.cell(r+1, c+1)
            sheet.row_dimensions[r+1].height = rows_height
            sheet.column_dimensions[get_column_letter(c+1)].width =\
                column_widths[c]
            cell.fill = generate_pattern_fill(COLORS[c])

    return workbook


def generate_columns_images(ref_workbook, table_params):
    """ Generate column images.
        :Arguments:
            ref_workbook: workbook:: table workbook
            table_params: dict:: randomly generated table parameters
        :Returns:
            list: list of column workbooks
    """
    ref_sheet = ref_workbook.active
    single_columns = []
    for c in range(table_params['columns_number']):
        new_workbook = Workbook()
        new_sheet = new_workbook.active
        for r in range(table_params['rows_number']):
            ref_cell = ref_sheet.cell(r+1, c+1)
            new_cell = new_sheet.cell(r+1, c+1)
            new_cell.value = copy(ref_cell.value)
            new_cell.border = copy(ref_cell.border)
            new_cell.font = copy(ref_cell.font)
            new_cell.alignment = copy(ref_cell.alignment)
            new_sheet.row_dimensions[r+1].height =\
                copy(ref_sheet.row_dimensions[r+1].height)
            new_sheet.column_dimensions[get_column_letter(c+1)].width =\
                copy(ref_sheet.column_dimensions[get_column_letter(c+1)].width)
        single_columns.append(copy(new_workbook))
    return single_columns


def save_data(path, table_wb, mask_wb, single_column_wb, words_list, table_nb):
    """ Save .xlsx, .png and .json files for table, mask, columns,
        column content etc.
        :Arguments:
            path: str:: path to save
            table_wb: workbook:: table workbook
            mask_wb workbook:: mask workbook
            single_column_wb: list:: column workbooks
            words_list: list of lists:: table content
            table_nb: int:: table number
        :Returns:
            saved files
    """
    if not path:
        path = "dataset/"
    if not exists(path):
        mkdir(path)
    table_name = str(table_nb) + "_table" + ".xlsx"
    table_img_name = str(table_nb) + "_table" + ".png"
    mask_name = str(table_nb) + "_mask" + ".xlsx"
    mask_img_name = str(table_nb) + "_mask" + ".png"

    table_wb.save(join(path, table_name))
    export_img(join(path, table_name), join(path, table_img_name))
    zero_padding(join(path, table_img_name), IMG_SHAPE)
    mask_wb.save(join(path, mask_name))
    export_img(join(path, mask_name), join(path, mask_img_name))
    zero_padding(join(path, mask_img_name), IMG_SHAPE, convert_to_gray=True)
    remove(join(path, mask_name))
    col_nb = 0
    for col, words in zip(single_column_wb, words_list):
        col_name = str(table_nb) + "_column_" + str(col_nb) + ".xlsx"
        col_img_name = str(table_nb) + "_column_" + str(col_nb) + ".png"
        col_text_name = str(table_nb) + "_column_" + str(col_nb) + ".json"
        col.save(join(path, col_name))
        export_img(join(path, col_name), join(path, col_img_name))
        zero_padding(join(path, col_img_name), IMG_COL_SHAPE)
        remove(join(path, col_name))
        with open(join(path, col_text_name), 'w') as outfile:
            json.dump(words, outfile)
        col_nb += 1


def zero_padding(img_name, img_size, convert_to_gray=False):
    """ Image zero padding to align image shapes to defined shape, common
        to all images.
        :Arguments:
            img_name: str:: image name
            img_size: tuple:: image shape
        :Returns:
            saved, zero padded image
    """
    img = imread(img_name)
    pad = ((0, (img_size[0]-img.shape[0]+1)),
           (0, (img_size[1]-img.shape[1]+1)),
           (0, 0))
    img = img[1:, 1:, :]
    img = np.pad(img, pad_width=pad, mode='constant', constant_values=(0))
    if convert_to_gray:
        imsave(img_name, rgb2labels(img))
    else:
        imsave(img_name, img)


def rgb2labels(img):
    """ Convert RGB mask to gray mask.
        :Arguments:
            img: numpy array:: image (mask) in RGB
        :Returns:
            saved, grayscale image (mask)
    """
    img = (rgb2gray(img)*255).astype('uint8')
    for label, color in enumerate(np.unique(img)[1:]):
        img[img == color] = label+1
    return img


def generate_dataset(table_nb, words_corpus, path=""):
    """ Generate single dataset, ie. .xlsx table, .png table, .png mask, .png
        columns, .json column content.
        :Arguments:
            table_nb: int:: table number
            words_corpus: dict:: words grouped by their length
            path: path to save folder
        :Returns:
            .xlsx table
            .png table
            .png mask
            .png columns
            .json column content
    """
    # for table_nb in table_nbs:  # for parallel
    # generate table parameters
    table_params = generate_table_params()
    # generate table content
    words_list = generate_words(words_corpus,
                                table_params['columns_number'],
                                table_params['rows_number'],
                                table_params['columns_type'])
    # generate column and row size
    column_widths = generate_columns_width(words_list, table_params)
    rows_height = generate_rows_height(table_params['font_size'])
    # generate table styles
    border = generate_border(table_params['line_style'],
                             table_params['is_border'],
                             table_params['is_partial_border'])
    font = generate_font(table_params['font_name'], table_params['font_size'])
    alignment = generate_alingment(table_params['horizontal_alingment'],
                                   table_params['vertical_alingment'])
    # generate table
    table_wb = generate_table(words_list, table_params, font, border,
                              alignment, rows_height, column_widths)
    mask_wb = generate_masks(table_params['columns_number'],
                             table_params['rows_number'], column_widths,
                             rows_height)
    single_columns_wb = generate_columns_images(table_wb, table_params)
    save_data(path, table_wb, mask_wb, single_columns_wb,
              words_list, table_nb)


def generate_dataset_parallel(table_nbs, words_corpus, path=""):
    """ Generate a batch of dataset, ie. .xlsx table, .png table, .png mask,
        .png columns, .json column content in parallel.
        :Arguments:
            table_nb: int:: table number
            words_corpus: dict:: words grouped by their length
            path: path to save folder
        :Returns:
            .xlsx table
            .png table
            .png mask
            .png columns
            .json column content
    """
    for table_nb in table_nbs:
        # generate table parameters
        table_params = generate_table_params()
        # generate table content
        words_list = generate_words(words_corpus,
                                    table_params['columns_number'],
                                    table_params['rows_number'],
                                    table_params['columns_type'])
        # generate column and row size
        columns_width = generate_columns_width(words_list, table_params)
        rows_height = generate_rows_height(table_params['font_size'])
        # generate table styles
        border = generate_border(table_params['line_style'],
                                 table_params['is_border'],
                                 table_params['is_partial_border'])
        font = generate_font(table_params['font_name'],
                             table_params['font_size'])
        alignment = generate_alingment(table_params['horizontal_alingment'],
                                       table_params['vertical_alingment'])
        # generate table
        table_wb = generate_table(words_list, table_params, font, border,
                                  alignment, rows_height, columns_width)
        mask_wb = generate_masks(table_params['columns_number'],
                                 table_params['rows_number'], columns_width,
                                 rows_height)
        single_columns_wb = generate_columns_images(table_wb, table_params)
        save_data(path, table_wb, mask_wb, single_columns_wb,
                  words_list, table_nb)


def make_chunks(lst, n):
    """ Split list into chunks.
        :Arguments:
            lst: list:: list to split
            n: int:: number of chunks
        :Returns:
            list of lists: list split into chunks.
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def dataset_generator(number_of_tables, parallel=True, save_path="",
                      config_path=""):
    """ Generate a set of tables for learning the ANN.
        :Arguments:
            number_of_tables: int:: number of tables to generate
            parallel: bool:: is computation is made parallel
            save_path: str:: path to save
            config_path: trs:: path to config files
    """
    words_corpus = define_words_list(config_path)
    if parallel:
        # synchronous
        pool = mp.Pool(mp.cpu_count())
        chunks = make_chunks([i for i in range(number_of_tables)], 10)
        [pool.apply(generate_dataset_parallel, args=(table_nbs, words_corpus,
                                                     save_path))
         for table_nbs in chunks]
    else:
        # serialize - slow
        for table_nb in range(number_of_tables):
            generate_dataset(table_nb, words_corpus)

    # asynchronous - fast, but error can occur
    # r = [pool.apply_async(generate_dataset_parallel,
    #                      args=(table_nbs, words_corpus))
    #     for table_nbs in chunks]
    # [p.get() for p in r]
    # pool.close()
    # pool.join()


if __name__ == "__main__":
    dataset_generator(10)
