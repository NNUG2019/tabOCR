import os
os.chdir("../../")
from matplotlib import pyplot as plt
from skimage.io import imread
from pkg.run_model import run_model
os.chdir("./notebooks/summary")


def display_4_imgs(path1, path2, path3, path4):
    plt.figure(figsize=(18,18), dpi=300)
    plt.subplot(2,2,1)
    plt.imshow(imread(path1), cmap=plt.cm.gray)
    plt.subplot(2,2,2)
    plt.imshow(imread(path2), cmap=plt.cm.gray)
    plt.subplot(2,2,3)
    plt.imshow(imread(path3))
    plt.subplot(2,2,4)
    plt.imshow(imread(path4))
    plt.show()


def display_2_imgs(path1, path2):
    plt.figure(figsize=(18,18), dpi=300)
    plt.subplot(1,2,1)
    plt.imshow(imread(path1), cmap=plt.cm.gray)
    plt.subplot(1,2,2)
    plt.imshow(imread(path2), cmap=plt.cm.gray)
    plt.show()
    
    
def display_3_imgs(path1, path2, path3):
    plt.figure(figsize=(18,18), dpi=300)
    plt.subplot(1,3,1)
    plt.imshow(imread(path1), cmap=plt.cm.gray)
    plt.subplot(1,3,2)
    plt.imshow(imread(path2), cmap=plt.cm.gray)
    plt.subplot(1,3,3)
    plt.imshow(imread(path3), cmap=plt.cm.gray)
    plt.show()


def show_prediction(model_name, model_type):
    os.chdir("./notebooks/summary")
    if model_type == "columns":
        img_test_path = "dataset/columns/img"
        mask_test_path = "dataset/columns/mask"
    elif model_type == "cells":
        img_test_path = "dataset/cells/img"
        mask_test_path = "dataset/cells/mask"
    else:
        raise ValueError("No such model!")
    for img_name, mask_name in zip(os.listdir(img_test_path),
                                   os.listdir(mask_test_path)):        
        run_model(model_name,
                  os.path.join(img_test_path, img_name),
                  os.path.join(mask_test_path, mask_name))
        print("\n\n------------------------------------------------------\n\n\n")
    os.chdir("../../")
