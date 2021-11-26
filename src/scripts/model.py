import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets, metrics, model_selection 
from sklearn.calibration import calibration_curve, CalibrationDisplay
import tensorflow as tf
import tensorflow_probability as tfp

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Model:
    def __init__(self, dataset_name = None, dataset_path = None, test_size=0.2):
        # Load and split dataset
        if dataset_path:
            data_df = pd.read_csv(dataset_path)
            dataset_name = dataset_path.split("/")[-1][:-4]
        else:
            data_df = pd.read_csv("src/data/{}/{}_data.csv".format(dataset_name, dataset_name))
            
        logger.info("Loaded {} dataset".format(dataset_name))
        X, y = data_df.iloc[:,1:], data_df.iloc[:,0]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=test_size)
        
    def train(self, model):
        logger.info("Training {}...".format(model))
        self.clf = model.fit(self.X_train, self.y_train)
        test_score = self.clf.score(self.X_test, self.y_test)
        logger.info("Accuracy of the model on test set: {}".format(test_score))
    
    def plot_clf(self, num_bins=10):
        # Plot AUC curves
        metrics.plot_roc_curve(self.clf, self.X_train, self.y_train)
        plt.title("AUC for Training set")
        metrics.plot_roc_curve(self.clf, self.X_test, self.y_test) 
        plt.title("AUC for Test set")
        # Calibration Plots
        self.plot_calibration(self.X_train, self.y_train, num_bins, "Training")
        self.plot_calibration(self.X_test, self.y_test, num_bins, "Test")
        
    def plot_calibration(self, X, y, num_bins=10, dataset_name="Training"):
        y_prob = self.clf.predict_proba(X)[:, 1]
        prob_true, prob_pred = calibration_curve(y, y_prob, n_bins=num_bins)
        disp = CalibrationDisplay(prob_true, prob_pred, y_prob)
        disp.plot()
        ece = self.computeECE(X, y, num_bins)
        plt.title("Calibration Curve for {} Data (ECE: {})".format(dataset_name, round(float(ece), 2)))
    
    def computeECE(self, X, y, num_bins):
        y_pred = self.clf.predict(X)
        y_train_tensor = tf.convert_to_tensor(y, dtype=tf.int64, name='labels_true')
        y_pred_tensor = tf.convert_to_tensor(y_pred, dtype=tf.int64)

        # Computing logit
        y_pred_proba = self.clf.predict_proba(X)
        logit_tensor = tf.convert_to_tensor(y_pred_proba, dtype=tf.float32, name='logits')

        return tfp.stats.expected_calibration_error(
            num_bins, logits=logit_tensor, labels_true=y_train_tensor, labels_predicted=None, name="logistic_regression"
        )