from keras.layers import (Conv2D, MaxPooling2D, Dropout, Input, concatenate,
                          Activation, Reshape, Conv2DTranspose,
                          BatchNormalization)
from keras.models import Model


def model_cell_segmentation(input_height, input_width, n_classes,
                            verbose=True):
    """ """

    img_input = Input(shape=(input_height, input_width, 3))
    conv1 = Conv2D(32, (3, 3), activation='relu', padding='same')(img_input)
    conv1 = Dropout(0.2)(conv1)
    conv1 = Conv2D(32, (3, 3), padding='same')(conv1)
    batch1 = BatchNormalization()(conv1)
    batch1 = Activation('relu')(batch1)
    pool1 = MaxPooling2D((4, 4))(batch1)

    conv2 = Conv2D(64, (3, 3), activation='relu', padding='same')(pool1)
    conv2 = Dropout(0.2)(conv2)
    conv2 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv2)
    batch2 = BatchNormalization()(conv2)
    batch2 = Activation('relu')(batch2)

    pool2 = MaxPooling2D((2, 2))(conv2)
    conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool2)
    conv3 = Dropout(0.2)(conv3)
    conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv3)

    u3 = Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(conv3)
    up1 = concatenate([u3, conv2], axis=-1)

    conv4 = Conv2D(64, (3, 3), activation='relu', padding='same')(up1)
    conv4 = Dropout(0.2)(conv4)
    conv4 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv4)

    u4 = Conv2DTranspose(32, (2, 2), strides=(4, 4), padding='same')(conv4)
    up2 = concatenate([u4, conv1], axis=-1)

    conv6 = Conv2D(32, (3, 3), activation='relu', padding='same')(up2)
    conv6 = Dropout(0.2)(conv6)
    conv6 = Conv2D(32, (3, 3), activation='relu', padding='same')(conv6)

    out = Conv2D(n_classes, (1, 1), padding='same')(conv6)

    out = Reshape((input_height*input_width, -1))(out)
    out = Activation('sigmoid')(out)

    model = Model(img_input, out)
    if verbose:
        model.summary()

    return model
