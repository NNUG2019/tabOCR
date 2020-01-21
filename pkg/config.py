from pkg.custom_metrics import mean_iou
from keras import optimizers


INPUT_HEIGHT = 512
INPUT_WIDTH = 1024
IMG_SIZE = (INPUT_HEIGHT, INPUT_WIDTH)
N_CLASSES = 2
BATCH_SIZE = 4
EPOCHS = 20
STEPS_PER_EPOCH = 1000
OPTIMIZER = optimizers.Adam()
LOSS = "binary_crossentropy"
METRICS = [mean_iou]

IMG_TEST_PATH = "datasets/dataset_table_resized/image_table_test_resized/"
MASK_TEST_PATH = \
    "datasets/dataset_table_resized/mask_binary_cell_test_resized/"
MODEL_PATH = "models/"
