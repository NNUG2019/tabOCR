import os


def save_csv(lst, path, sep=','):
    """

    save_csv generates and saves in path directory a <index>.csv file for each file in lst. Important! Rows in csv file
    are equivalent to columns in files saved by full_imager.

    :param lst: Three dimensional list of strings in format lst[file][row][column].
    :param path: Path to the target directory for saved files.
    :param sep: Separator to be inserted between cells in row.
    :return:
    """
    counter = 0
    for f in lst:
        txt = ''
        for l in f:
            for w in l:
                txt += w + sep
            txt = txt[:-1]
            txt += '\n'
        txt = txt[:-1]
        with open(os.path.join(path, str(counter) + '.csv'), 'w') as out:
            out.write(txt)
        counter += 1
