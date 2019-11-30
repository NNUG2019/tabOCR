from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Border, Side, Font, PatternFill
from random import choices, choice
import excel2img as e2i
import os

from colorizer import colorizer


def full_imager(lst, path):
    """

    full_imager is major data generating function. It generates 6 files for each file string set in lst parameter:
        a<index>.xlsx - excel file containing table with strings
        a<index>.bmp - a image of table file
        b<index>.xlsx - excel file containing masked columns from table file
        b<index>.bmp - a image of column mask file
        c<index>.xlsx - excel file containing masked cells from table file
        c<index>.bmp - a image of cell mask file
    They are saved in path directory.

    :param lst: Three dimensional list of strings in format lst[file][column][row].
    :param path: Path to the target directory for saved files.
    :return:
    """
    colors = colorizer()
    borders = [
        Side(border_style="thin", color="000000"),
        Side(border_style="thin", color="FF0000"),
        Side(border_style="thin", color="00FF00"),
        Side(border_style="thin", color="0000FF"),
        Side(border_style="thin", color="FFFFFF"),
        Side(border_style="medium", color="000000"),
        Side(border_style="medium", color="FF0000"),
        Side(border_style="medium", color="00FF00"),
        Side(border_style="medium", color="0000FF"),
        Side(border_style="medium", color="FFFFFF"),
        Side(border_style="thick", color="000000"),
        Side(border_style="thick", color="FF0000"),
        Side(border_style="thick", color="00FF00"),
        Side(border_style="thick", color="0000FF"),
        Side(border_style="thick", color="FFFFFF")
    ]
    blank_side = Side()
    blank_border = Border(top=blank_side, left=blank_side, right=blank_side, bottom=blank_side)
    counter = 0
    for f in lst:
        i = 0
        main_book = Workbook()
        main_sheet = main_book.active
        column_book = Workbook()
        column_sheet = column_book.active
        cell_book = Workbook()
        cell_sheet = cell_book.active
        for l in f:
            j = 0
            width_of_column = 0

            # Setting column values:
            column_color = colors[i]
            column_fill = PatternFill(patternType='solid', fill_type='solid', fgColor=column_color)

            for w in l:
                # Setting cell values:
                    # 17 so the color won't repeat!
                cell_color = colors[17*i+j]
                cell_fill = PatternFill(patternType='solid', fill_type='solid', fgColor=cell_color)

                # Generating table sheet:
                selected_borders = choices(borders, k=4)
                working_cell = main_sheet.cell(row=j+1, column=i+1)
                working_cell.value = w
                working_cell.border = Border(top=selected_borders[0], left=selected_borders[1],
                                             bottom=selected_borders[2], right=selected_borders[3])
                working_cell.font = Font(name=choice(["Calibri", "Arial", "TimesNewRoman"]),
                                         bold=choice([True, False]),
                                         italic=choice([True, False]),
                                         size=11,
                                         color=choice(colors[1:]))

                # Adjusting column_width value:
                width_of_column = max(width_of_column, len(str(working_cell.value))*1.5)

                # Generating column mask sheet:
                working_cell = column_sheet.cell(row=j+1, column=i+1)
                working_cell.border = blank_border
                working_cell.fill = column_fill

                # Generating cell mask sheet:
                working_cell = cell_sheet.cell(row=j+1, column=i+1)
                working_cell.border = blank_border
                working_cell.fill = cell_fill

                j += 1

            # Setting correct column widths in sheets:
            main_sheet.column_dimensions[get_column_letter(i+1)].width = width_of_column
            column_sheet.column_dimensions[get_column_letter(i+1)].width = width_of_column
            cell_sheet.column_dimensions[get_column_letter(i+1)].width = width_of_column
            i += 1

        # Saving table sheet:
        main_pth = os.path.join(path, 'a' + str(counter) + '.xlsx')
        main_book.save(main_pth)
        e2i.export_img(main_pth, os.path.join(path, 'a' + str(counter) + '.bmp'))

        # Saving column mask sheet:
        column_pth = os.path.join(path, 'b' + str(counter) + '.xlsx')
        column_book.save(column_pth)
        e2i.export_img(column_pth, os.path.join(path, 'b' + str(counter) + '.bmp'))

        # Saving cell mask sheet:
        cell_pth = os.path.join(path, 'c' + str(counter) + '.xlsx')
        cell_book.save(cell_pth)
        e2i.export_img(cell_pth, os.path.join(path, 'c' + str(counter) + '.bmp'))

        counter += 1
