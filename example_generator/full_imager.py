from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Border, Side, Font
from random import choices, choice
import excel2img as e2i
import os

from colorizer import colorizer


def full_imager(lst, path):
    counter = 0
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
    for f in lst:
        i = 0
        book = Workbook()
        sheet = book.active
        for l in f:
            j = 0
            col_wid = 0
            for w in l:
                selected_borders = choices(borders, k=4)
                cell = sheet.cell(row=j+1, column=i+1)
                cell.value = w
                cell.border = Border(top=selected_borders[0], left=selected_borders[1],
                                     bottom=selected_borders[2], right=selected_borders[3])
                cell.font = Font(name=choice(["Calibri", "Arial", "TimesNewRoman"]),
                                 bold=choice([True, False]),
                                 italic=choice([True, False]),
                                 size=11,
                                 color=choice(colors[1:]))
                col_wid = max(col_wid, len(str(cell.value))*1.5)
                j += 1
            sheet.column_dimensions[get_column_letter(i+1)].width = col_wid
            i += 1

        pth = os.path.join(path, str(counter) + '.xlsx')
        book.save(pth)
        e2i.export_img(pth, os.path.join(path, str(counter) + '.bmp'))
        counter += 1
