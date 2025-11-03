import os

DATASET_PATH = "dataset"

CLASSES = ["Flood", "Fire"]

TRAIN_SPLIT = 0.75
VAL_SPLIT = 0.1
TEST_SPLIT = 0.25

MIN_LR = 2e-7
MAX_LR = 2e-5
BATCH_SIZE = 4
STEP_SIZE = 8
CLR_METHOD = "triangular"
NUM_EPOCHS = 40

MODEL_PATH = os.path.sep.join(["output", "fire.model"])

LRFIND_PLOT_PATH = os.path.sep.join(["output", "lrfind_plot.png"])
TRAINING_PLOT_PATH = os.path.sep.join(["output", "training_plot.png"])
CLR_PLOT_PATH = os.path.sep.join(["output", "clr_plot.png"])