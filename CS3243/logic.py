import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn import datasets
import pandas as pd
from sklearn.linear_model import LogisticRegression

def sigmoid(z):
    return 1.0 / (1 + np.exp(-z))


def prediction(theta, X):
    predictions = np.zeros(X.shape[0], np.float)
    for i in range(len(X)):
        predictions[i] = sigmoid(np.dot(theta, X[i]))

    return predictions


def log_likelihood(X, y, theta):
    likelihood = 0.0
    m = X.shape[0]
    Z = prediction(theta, X)
    for i in range(m):
        likelihood -= y[i] * np.log(Z[i]) + (1 - y[i]) * np.log(1 - Z[i])

    return likelihood / m


def gradient(X, y, theta):
    m = X.shape[0]
    gradient = 1 / m * np.dot(X.T, prediction(theta, X) - y)

    return gradient


def logistic_regression(X, Y, num_steps, learning_rate, verbose):
    # Add the bias
    bias = np.ones((X.shape[0], 1))
    X = np.concatenate((bias, X), axis=1)

    # Initialize the weights
    weights = np.zeros(X.shape[1])

    # Training with gradient descent
    for step in range(num_steps):

        weights -= learning_rate * gradient(X, Y, weights)

        # Print log-likelihood every step
        cost = log_likelihood(X, Y, weights)
        if verbose and step % 1000 == 0:
            print('Number of iterations: {}; cost: {:.5f}'.format(step, cost))

    return weights


# Load the original dataset
iris = datasets.load_iris()

# Obtain the training data
X = iris.data[:, :2]
y = (iris.target != 0) * 1

weights = logistic_regression(X, y, num_steps = 300000, learning_rate = 0.1, verbose = True)


