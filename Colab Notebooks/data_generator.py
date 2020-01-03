from keras.utils import Sequence
from skimage.transform import resize
import numpy as np
import cv2
from matplotlib import pyplot as plt


class image_generator(Sequence):

    def __init__(self,
                 image_filenames,
                 mask_filenames,
                 batch_size,
                 img_size,
                 n_calsses,
                 loss='categorical_crossentropy',
                 no_reshape=False):
        self.image_filenames = image_filenames
        self.mask_filenames = mask_filenames
        self.batch_size = batch_size
        self.height = img_size[0]
        self.width = img_size[1]
        self.n_calsses = n_calsses
        self.no_reshape = no_reshape
        self.loss = loss

    def __len__(self):
        return int(np.ceil(len(self.image_filenames) / float(self.batch_size)))

    def get_img_array(self, file_name):
        img = cv2.imread(file_name, 1)
        return resize(img, (self.height, self.width, 3))

    def get_segmentation_mask(self, file_name):
        img = cv2.imread(file_name, 1)
        img = cv2.resize(img, (self.height, self.width),
                         interpolation=cv2.INTER_NEAREST)
        img = img[:, :, 0]
        seg_labels = np.zeros((self.width, self.height, self.n_calsses))
        for c in range(self.n_calsses):
            seg_labels[:, :, c] = (img == c).astype(int)
        if not self.no_reshape:
            seg_labels = np.reshape(seg_labels,
                                    (self.height*self.width, self.n_calsses))
        return seg_labels

    def __getitem__(self, idx):
        batch_x = self.image_filenames[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_y = self.mask_filenames[idx * self.batch_size:(idx + 1) * self.batch_size]

        if self.loss == 'categorical_crossentropy':
            return (np.array([self.get_img_array(file_name)
                              for file_name in batch_x]),
                    np.array([self.get_segmentation_mask(file_name)
                              for file_name in batch_y]))
        else:
            return (np.array([self.get_img_array(file_name)
                              for file_name in batch_x]),
                    np.array([self.get_segmentation_mask(file_name)
                              for file_name in batch_y]))


def predict(model, file_name_img, file_name_mask, input_height, input_width,
            n_classes):
    img_test = cv2.imread(file_name_img, 1)
    img_mask = cv2.imread(file_name_mask, 0)
    img_mask = cv2.resize(img_mask, (input_height, input_width),
                          interpolation=cv2.INTER_NEAREST)
    img_test = cv2.resize(img_test, (input_height, input_width),
                          interpolation=cv2.INTER_NEAREST)
    img_test = np.expand_dims(img_test, axis=0)
    mask_pred = model.predict(img_test)
    mask_pred = mask_pred.reshape((input_height, input_width, n_classes)).\
        argmax(axis=2)
    plt.figure(figsize=(32, 32))
    plt.subplot(1, 3, 1)
    plt.imshow(img_test[0])
    plt.subplot(1, 3, 2)
    plt.imshow(img_mask)
    plt.subplot(1, 3, 3)
    plt.imshow(mask_pred)
    plt.show()
