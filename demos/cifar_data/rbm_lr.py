"""This script compares results of running logistic regression on 
- raw cifar images 
vs
- features extracted by RBM from cifar images.

This code is lifted from scikit learn docs [1].

[1] - http://scikit-learn.org/stable/auto_examples/plot_rbm_logistic_classification.html

"""

import math
import numpy as np
import matplotlib.pyplot as plt

from sklearn import linear_model, datasets, metrics
from sklearn.cross_validation import train_test_split
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline

import npimage
import dataset


def main():
    cifar = dataset.load(10000)
    X, Y = cifar.data, cifar.target
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y,
                                                        test_size=0.2,
                                                        random_state=0)
    logistic = linear_model.LogisticRegression(C=6000.0)
    rbm = BernoulliRBM(n_components=100,
                       learning_rate=0.025,
                       batch_size=10,
                       n_iter=100,
                       verbose=True)

    classifier = Pipeline(steps=[('rbm', rbm), ('logistic', logistic)])

    # Training RBM-Logistic Pipeline
    classifier.fit(X_train, Y_train)

    # Training Logistic regression
    logistic_classifier = linear_model.LogisticRegression(C=100.0)
    logistic_classifier.fit(X_train, Y_train)

    Y_predicted_rbm = classifier.predict(X_test)
    Y_predicted_raw = logistic_classifier.predict(X_test)

    # Evaluate classifiers
    print()
    print("Logistic regression using RBM features:\n%s\n" % (
        metrics.classification_report(
            Y_test,
            Y_predicted_rbm,
            target_names=cifar.target_names)))

    print("Logistic regression using raw pixel features:\n%s\n" % (
        metrics.classification_report(
            Y_test,
            Y_predicted_raw,
            target_names=cifar.target_names)))

    print("Confusion matrix RBM features:\n%s" % metrics.confusion_matrix(Y_test, Y_predicted_rbm))
    print("Confusion matrix raw pixel features:\n%s" % metrics.confusion_matrix(Y_test, Y_predicted_raw))

    # Plot RBM features
    plot(rbm, 100)


def plot(rbm, n_images=None):
    dim = int(math.sqrt(rbm.n_components if n_images is None else n_images))

    plt.figure(figsize=(8.2, 8))
    for i, comp in enumerate(rbm.components_):
        if i >= dim**2:
            break;
        plt.subplot(dim, dim, i + 1)
        plt.imshow(npimage.unflatten(comp))
        plt.xticks(())
        plt.yticks(())
        plt.suptitle('%d components extracted by RBM' % (rbm.n_components,), fontsize=16)
        plt.subplots_adjust(0.08, 0.02, 0.92, 0.85, 0.08, 0.23)
    plt.show()


if __name__=="__main__":
    main()
