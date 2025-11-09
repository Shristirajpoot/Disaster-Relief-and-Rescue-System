# import the necessary packages
import os

# initialize the path to the input directory containing our dataset
# of images
DATASET_PATH = "flood_dataset"

# initialize the class labels in the dataset
CLASSES = ["Flood", "Wildfire"]

# define the size of the training, validation (which comes from the
# train split), and testing splits, respectively
TRAIN_SPLIT = 0.75
VAL_SPLIT = 0.1
TEST_SPLIT = 0.25

# define the minimum learning rate, maximum learning rate, batch size,
# step size, CLR method, and number of epochs
MIN_LR = 2e-7
MAX_LR = 2e-5
BATCH_SIZE = 4
STEP_SIZE = 8
CLR_METHOD = "triangular"
NUM_EPOCHS = 40

# set the path to the serialized model after training
MODEL_PATH = os.path.sep.join(["output", "natural_disaster_2.model"])

# define the path to the output learning rate finder plot, training
# history plot and cyclical learning rate plot
LRFIND_PLOT_PATH = os.path.sep.join(["output", "lrfind_plot.png"])
TRAINING_PLOT_PATH = os.path.sep.join(["output", "training_plot.png"])
CLR_PLOT_PATH = os.path.sep.join(["output", "clr_plot.png"])