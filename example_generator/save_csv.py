import os


def save_csv(lst, path, sep=','):
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
