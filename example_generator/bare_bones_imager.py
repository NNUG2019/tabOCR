from openpyxl import Workbook
from openpyxl.styles import Border, Side
import excel2img as e2i
import os


def bare_bones_imager(lst, path):
    book = Workbook()
    sheet = book.active
    counter = 0
    red = Side(border_style="thin", color="FFFFFF")
    black = Side(border_style="thin", color="FFFFFF")
    for f in lst:
        i = 0
        for l in f:
            j = 0
            for w in l:
                sheet.cell(row=i+1, column=j+1).value = w
                sheet.cell(row=i+1, column=j+1).border = Border(top=red, left=red, bottom=black, right=black)
                j += 1
            i += 1

        pth = os.path.join(path, str(counter) + '.xlsx')
        book.save(pth)
        e2i.export_img(pth, os.path.join(path, str(counter) + '.bmp'))
        counter += 1
