from keras.models import load_model
import os
# os.chdir("../")
from pkg.custom_metrics import mean_iou  # noqa
from pkg.models_utils import make_predictions  # noqa
from pkg.config import IMG_TEST_PATH, MASK_TEST_PATH, MODEL_PATH  # noqa


def load_model_from_file(model_path):
    dependencies = {"mean_iou": mean_iou}
    return load_model(model_path, custom_objects=dependencies, compile=False)


def run_model(model_path, img_test_path, mask_test_path):
    """ """
    model = load_model_from_file(model_path)
    make_predictions(model, img_test_path, mask_test_path)


if __name__ == "__main__":
    print(os.getcwd())
    img_name = "5_table.png"
    model_name = "table_simple_cells.h5"
    img_test_path = os.path.join(IMG_TEST_PATH, img_name)
    mask_test_path = os.path.join(MASK_TEST_PATH, img_name)
    model_path = os.path.join(MODEL_PATH, model_name)
    run_model(model_path, img_test_path, mask_test_path)
