from keras.callbacks import ReduceLROnPlateau, EarlyStopping
# from keras.callbacks import ModelCheckpoint
import tensorflow.compat.v1 as tf
import numpy as np
import cv2
import os
from pkg.plots import plot_prediction
from pkg.config import (IMG_TEST_PATH, MASK_TEST_PATH, INPUT_HEIGHT,
                        INPUT_WIDTH, N_CLASSES)


class DisplayCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        make_predictions()
        print('\nPrediction after epoch {}\n'.format(epoch+1))


def define_callbacks():
    # save model after each epoch if metric will improve
    # filepath = os.path.join(MODEL_PATH, "model_table_cells_checkpoint.hdf5")
    # checkpoint = ModelCheckpoint(filepath, monitor='mean_iou', verbose=1,
    #                             save_best_only=True, mode='max', period=1)
    # reduces learning rate on plateau
    lr_reducer = ReduceLROnPlateau(factor=0.1,
                                   cooldown=2,
                                   monitor='mean_iou',
                                   patience=2, verbose=1,
                                   min_lr=0.1e-7)
    # stop learining as metric on validatopn stop increasing
    early_stopping = EarlyStopping(patience=5, verbose=1, mode='auto')

    return [lr_reducer, early_stopping, DisplayCallback()]


def make_predictions(model="", img_path="", mask_path=""):
    """ Make prediction. """

    # load image and mask
    if not img_path:
        img = cv2.imread(os.path.join(IMG_TEST_PATH, "5_table.png"), 1)
    else:
        img = cv2.imread(img_path, 1)
    if not mask_path:
        mask = cv2.imread(os.path.join(MASK_TEST_PATH), 1)
    else:
        mask = cv2.imread(mask_path, 1)
    # prepare image
    img = cv2.resize(img, (INPUT_WIDTH, INPUT_HEIGHT),
                     interpolation=cv2.INTER_NEAREST)
    img = np.expand_dims(img, axis=0).astype('float32')
    mask = cv2.resize(mask, (INPUT_WIDTH, INPUT_HEIGHT),
                      interpolation=cv2.INTER_NEAREST)
    # predict
    mask_pred = model.predict(img)
    # postprocess predicted mask
    mask_pred = mask_pred.reshape((INPUT_HEIGHT, INPUT_WIDTH, N_CLASSES)).\
        argmin(axis=2)
    # show prediction
    plot_prediction(img, mask, mask_pred)


def train_model(model, train_generator, val_generator, optimizer, loss,
                metrics, epochs=20, steps_per_epoch=1000):
    print("Compile model...")
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
    callbacks = define_callbacks()
    print("Train NN...")
    history = model.fit_generator(train_generator,
                                  validation_data=val_generator,
                                  epochs=epochs,
                                  steps_per_epoch=steps_per_epoch,
                                  callbacks=callbacks,
                                  workers=2,
                                  use_multiprocessing=True,
                                  verbose=1)
    return history
