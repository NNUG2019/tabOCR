from keras.utils import Sequence
import numpy as np
import os
import cv2


class image_generator(Sequence):
    """ Training data generator. """
    def __init__(self, image_fn, mask_fn, batch_size, img_size, n_calsses,
                 loss, no_reshape=False):
        self.image_fn, self.mask_fn = image_fn, mask_fn
        self.batch_size = batch_size
        self.height, self.width = img_size
        self.n_calsses = n_calsses
        self.no_reshape = no_reshape
        self.loss = loss

    def __len__(self):
        return int(np.ceil(len(self.image_fn) / float(self.batch_size)))

    def get_img_array(self, file_name):
        """ Prepare image. """
        img = cv2.imread(file_name, 1)
        img = cv2.resize(img, (self.width, self.height))/255
        return img.astype('float32')

    def get_segmentation_mask(self, file_name, invert_mask=True, sparse=False):
        """ Prepare mask. """
        mask = cv2.imread(file_name, 1)
        # opencv has different convention: column x row instead of row x column
        mask = cv2.resize(mask, (self.width, self.height),
                          interpolation=cv2.INTER_NEAREST)[:, :, 0]
        if invert_mask:
            mask = mask.max() - mask
        if sparse:
            mask = np.reshape(mask, (self.height*self.width))
            return np.expand_dims(mask, 2).astype('uint8')

        seg_labels = np.zeros((self.height, self.width, self.n_calsses))
        for c in range(self.n_calsses):
            seg_labels[:, :, c] = (mask == c).astype(int)
        if not self.no_reshape:
            seg_labels = np.reshape(seg_labels,
                                    (self.height*self.width, self.n_calsses))
        return seg_labels.astype('bool')

    def __getitem__(self, idx):
        """ Generate a batch of training data - image and mask. """
        batch_x = self.image_fn[idx*self.batch_size:(idx + 1)*self.batch_size]
        batch_y = self.mask_fn[idx*self.batch_size:(idx + 1)*self.batch_size]
        if ((self.loss == 'categorical_crossentropy') or
                (self.loss == 'binary_crossentropy')):
            return (np.array([self.get_img_array(file_name)
                              for file_name in batch_x]),
                    np.array([self.get_segmentation_mask(file_name)
                              for file_name in batch_y]))
        elif self.loss == 'sparse_categorical_crossentropy':
            return (np.array([self.get_img_array(file_name)
                              for file_name in batch_x]),
                    np.array([self.get_segmentation_mask(file_name,
                                                         sparse=True)
                              for file_name in batch_y]))
        else:
            raise KeyError(
                "Such type of loss function: '{}' is not supported".
                format(self.loss))


def generate_images(img_train_path, img_val_path, mask_train_path,
                    mask_val_path, batch_size, img_size, n_classes, loss):
    def _make_filenames(path):
        return list(map(lambda s: os.path.join(path, s),
                        sorted(os.listdir(path))))

    image_filenames = _make_filenames(img_train_path)
    mask_filenames = _make_filenames(img_val_path)
    image_filenames_val = _make_filenames(mask_train_path)
    mask_filenames_val = _make_filenames(mask_val_path)

    train_generator = image_generator(image_filenames,
                                      mask_filenames,
                                      batch_size=batch_size,
                                      img_size=img_size,
                                      n_calsses=n_classes,
                                      loss=loss)
    val_generator = image_generator(image_filenames_val,
                                    mask_filenames_val,
                                    batch_size=batch_size,
                                    img_size=img_size,
                                    n_calsses=n_classes,
                                    loss=loss)

    return train_generator, val_generator
