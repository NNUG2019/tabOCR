from openpyxl import Workbook
import excel2img as e2i
import os


def bare_bones_imager(lst, path):
    book = Workbook()
    sheet = book.active
    counter = 0
    for f in lst:
        i = 0
        for l in f:
            j = 0
            for w in l:
                sheet.cell(row=i+1, column=j+1).value = w
                j += 1
            i += 1

        pth = os.path.join(path, str(counter) + '.xlsx')
        book.save(pth)
        e2i.export_img(pth, os.path.join(path, str(counter) + '.bmp'))
        counter += 1
