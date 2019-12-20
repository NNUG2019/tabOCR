from excel2img import export_img
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from os.path import join, exists
from os import mkdir
from os import remove
from shutil import rmtree
from copy import copy
import json
from skimage.io import imread, imsave
from skimage.color import rgb2gray
import numpy as np
from parameters_generator import (generate_table_params, IMG_SHAPE,
                                  generate_header_params, generate_rows_height,
                                  generate_columns_width, IMG_COL_SHAPE,
                                  MAX_ROW_HEIGHT, PIXEL_ROW)
from style_generator import (generate_border, generate_font,
                             generate_alingment, generate_pattern_fill)
from word_generator import generate_words, define_words_list
import multiprocessing as mp
import logging
import warnings
import traceback

warnings.simplefilter("ignore", UserWarning)

logger = logging.getLogger("logs")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
fh = logging.FileHandler('logs.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)


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
    colors = generate_colors(columns_number, rows_number)
    for c in range(columns_number):
        for r in range(rows_number):
            cell = sheet.cell(r+1, c+1)
            sheet.row_dimensions[r+1].height = rows_height
            sheet.column_dimensions[get_column_letter(c+1)].width =\
                column_widths[c]
            cell.fill = generate_pattern_fill(colors[c])

    return workbook


def generate_colors(columns_number, rows_number):
    """ """
    for c in range(columns_number):
        for r in range(rows_number):
            colors = ['#%02x%02x%02x' % (c, c, c)
                      for c in range(5, 5*columns_number*rows_number+5, 5)]
    return list(map(lambda s: s.strip('#').upper(), colors))


def generate_cell_mask(columns_number, rows_number, column_widths,
                       rows_height):
    """ """
    colors = generate_colors(columns_number, rows_number)
    single_columns = []
    for c in range(columns_number):
        workbook = Workbook()
        sheet = workbook.active
        for r in range(rows_number):
            cell = sheet.cell(r+1, c+1)
            sheet.row_dimensions[r+1].height = rows_height
            sheet.column_dimensions[get_column_letter(c+1)].width =\
                column_widths[c]
            cell.fill = generate_pattern_fill(colors[r])
        single_columns.append(copy(workbook))
    return single_columns


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


def generate_cells_images(ref_workbook, table_params):
    """ Generate column images.
        :Arguments:
            ref_workbook: workbook:: table workbook
            table_params: dict:: randomly generated table parameters
        :Returns:
            list: list of column workbooks
    """
    ref_sheet = ref_workbook.active
    cells = []
    for c in range(table_params['columns_number']):
        single_cells = []
        for r in range(table_params['rows_number']):
            new_workbook = Workbook()
            new_sheet = new_workbook.active
            ref_cell = ref_sheet.cell(r+1, c+1)
            new_cell = new_sheet.cell(r+1, c+1)
            new_cell.value = copy(ref_cell.value)
            new_cell.font = copy(ref_cell.font)
            new_cell.alignment = copy(ref_cell.alignment)
            new_sheet.row_dimensions[r+1].height =\
                copy(ref_sheet.row_dimensions[r+1].height)
            new_sheet.column_dimensions[get_column_letter(c+1)].width =\
                copy(ref_sheet.column_dimensions[get_column_letter(c+1)].width)
            single_cells.append(copy(new_workbook))
        cells.append(single_cells)
    return cells


def save_data(path, table_wb, mask_wb, cell_mask, single_column_wb,
              single_cells_wb, words_list, table_nb):
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
    dir_name = join(path, str(table_nb))
    if exists(dir_name):
        rmtree(dir_name)
    mkdir(dir_name)

    table_name = str(table_nb) + "_table" + ".xlsx"
    table_img_name = str(table_nb) + "_table" + ".png"
    mask_name = str(table_nb) + "_mask" + ".xlsx"
    mask_img_name = str(table_nb) + "_mask" + ".png"

    table_wb.save(join(dir_name, table_name))
    export_img(join(dir_name, table_name), join(dir_name, table_img_name))
    zero_padding(join(dir_name, table_img_name), IMG_SHAPE)
    mask_wb.save(join(dir_name, mask_name))
    export_img(join(dir_name, mask_name), join(dir_name, mask_img_name))
    zero_padding(join(dir_name, mask_img_name), IMG_SHAPE, convert_to_gray=True)
    remove(join(dir_name, mask_name))
    col_nb = 0
    for col, col_mask, words in zip(single_column_wb, cell_mask, words_list):
        col_name = str(table_nb) + "_column_" + str(col_nb) + ".xlsx"
        col_img_name = str(table_nb) + "_column_" + str(col_nb) + ".png"
        col_text_name = str(table_nb) + "_column_" + str(col_nb) + ".json"

        col_mask_name = str(table_nb) + "_column_mask" + str(col_nb) + ".xlsx"
        col_mask_img_name =\
            str(table_nb) + "_column_mask_" + str(col_nb) + ".png"

        col.save(join(dir_name, col_name))
        export_img(join(dir_name, col_name), join(dir_name, col_img_name))
        zero_padding(join(dir_name, col_img_name), IMG_COL_SHAPE)
        remove(join(dir_name, col_name))

        col_mask.save(join(dir_name, col_mask_name))
        export_img(join(dir_name, col_mask_name), join(dir_name, col_mask_img_name))
        zero_padding(join(dir_name, col_mask_img_name), IMG_COL_SHAPE)
        remove(join(dir_name, col_mask_name))

        with open(join(dir_name, col_text_name), 'w') as outfile:
            json.dump(words, outfile)
        col_nb += 1
    cell_nb = 0
    col = 0
    row = 0
    for cells, words in zip(single_cells_wb, words_list):
        for cell, word in zip(cells, words):
            cell_name = str(table_nb) + "_cell_" + str(col) + "_" + str(row) + ".xlsx"
            cell_img_name = str(table_nb) + "_cell_" + str(col) + "_" + str(row) + ".png"
            cell_text_name = str(table_nb) + "_cell_" + str(col) + "_" + str(row) + ".json"
            cell.save(join(dir_name, cell_name))
            export_img(join(dir_name, cell_name), join(dir_name, cell_img_name))
            zero_padding(join(dir_name, cell_img_name),
                         (int(MAX_ROW_HEIGHT*PIXEL_ROW), IMG_COL_SHAPE[1]))
            remove(join(dir_name, cell_name))
            with open(join(dir_name, cell_text_name), 'w') as outfile:
                json.dump(word, outfile)
            cell_nb += 1
            row += 1
        col += 1


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
    try:
        img = np.pad(img, pad_width=pad, mode='constant', constant_values=(0))
    except Exception as e:
        logger.error("Wrong image size: img.shape: {img.shape}, img_size: {}")
        raise
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
    single_cells_wb = generate_cells_images(table_wb, table_params)
    save_data(path, table_wb, mask_wb, single_columns_wb, single_cells_wb,
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
        logger.info("Generate table no. {}".format(table_nb))
        should_repeat = True
        while should_repeat:
            try:
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
                cell_mask = generate_cell_mask(table_params['columns_number'],
                                               table_params['rows_number'],
                                               columns_width, rows_height)
                single_columns_wb = generate_columns_images(table_wb, table_params)
                single_cells_wb = generate_cells_images(table_wb, table_params)
                save_data(path, table_wb, mask_wb, cell_mask,
                          single_columns_wb, single_cells_wb, words_list,
                          table_nb)
                should_repeat = False
                logger.info("Table was generated succesfuly")
            except Exception as e:
                tb = traceback.format_exc()
                logger.error(tb)


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
    dataset_generator(
        10,
        # save_path = "F://studia//Doktorat//Badania//tabOCR//test_dataset"
        # config_path = "...//config"
    )
