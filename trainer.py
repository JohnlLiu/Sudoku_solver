from tensorflow.keras.optimizers import Adam
from tensorflow.keras.datasets import mnist
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report
import argparse
import learner

ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True, help="path to output model after training")
args = vars(ap.parse_args())

