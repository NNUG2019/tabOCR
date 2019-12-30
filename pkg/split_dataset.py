import os
import re
import shutil


def split_dataset(dataset_path, new_dataset_path):
    if not os.path.exists(new_dataset_path):
        os.mkdir(new_dataset_path)
    img_path = os.path.join(new_dataset_path, "img_table")
    mask_column_path = os.path.join(new_dataset_path, "img_mask_column")
    mask_cell_path = os.path.join(new_dataset_path, "img_mask_cell")
    mask_column_cells_path = os.path.join(new_dataset_path, "img_mask_column_cells")
    folders = [img_path, mask_column_path, mask_cell_path, mask_column_cells_path]
    for path in folders:
        if not os.path.exists(path):
            os.mkdir(path)

    for path, folders, files in os.walk(dataset_path):
        for f in files:
            if f.endswith('table.png'):
                shutil.copyfile(os.path.join(path, f), os.path.join(img_path, f))
            if f.endswith('mask.png'):
                shutil.copyfile(os.path.join(path, f), os.path.join(mask_column_path, f))
                os.rename(os.path.join(mask_column_path, f), os.path.join(mask_column_path, f.replace("mask", "table")))
            if f.endswith('mask_cell.png'):
                shutil.copyfile(os.path.join(path, f), os.path.join(mask_cell_path, f))
                os.rename(os.path.join(mask_cell_path, f), os.path.join(mask_cell_path, f.replace("mask_cell", "table")))
            if re.match(".*column_mask_[0-9].png$", f):
                shutil.copyfile(os.path.join(path, f), os.path.join(mask_column_cells_path, f))
                os.rename(os.path.join(mask_column_cells_path, f), os.path.join(mask_column_cells_path, f.replace("column_mask", "table")))


if __name__ == "__main__":
    new_dataset_path = "dataset_test2"
    dataset_path = "dataset_test"
    split_dataset(dataset_path, new_dataset_path)
