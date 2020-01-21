from matplotlib import pyplot as plt


def plot_prediction(img, mask, mask_pred):
    """ Plot input image and expected and predicted masks. """

    plt.figure(figsize=(24, 24), dpi=150)
    plt.subplot(1, 3, 1)
    plt.title("Input image")
    plt.imshow(((img[0]/img[0].max())*255).astype('uint8'))
    plt.subplot(1, 3, 2)
    plt.title("Expected (ground truth) mask")
    plt.imshow(mask, cmap=plt.cm.gray)
    plt.subplot(1, 3, 3)
    plt.title("Predicted mask")
    plt.imshow((mask_pred*255).astype('uint8'), cmap=plt.cm.gray)
    plt.show()
