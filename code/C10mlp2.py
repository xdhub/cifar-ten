import os
import sys
import time

import numpy

import theano
import theano.tensor as T

import dataset as ds

import cifarDirectories
sys.path.append(cifarDirectories.DeepLearningTutorialsCode())

from mlp import MLP
from hyperparameter import HyperparametersMLP

def test_mlp(dataset, hyper):
    train_set_x, train_set_y = dataset.sharedTrain
    valid_set_x, valid_set_y = dataset.sharedValid
    test_set_x, test_set_y = dataset.sharedTest

    n_train_batches = train_set_x.get_value(borrow=True).shape[0] / hyper.batchSize
    n_valid_batches = valid_set_x.get_value(borrow=True).shape[0] / hyper.batchSize
    n_test_batches = test_set_x.get_value(borrow=True).shape[0] / hyper.batchSize

    validationFrequency = min(n_train_batches, hyper.patience / 2)

    print '... building the model'

    # allocate symbolic variables for the data
    index = T.lscalar()  # index to a [mini]batch
    x = T.matrix('x')  # the data is presented as rasterized images
    y = T.ivector('y')  # the labels are presented as 1D vector of
                        # [int] labels

    rng = numpy.random.RandomState(1234)

    # construct the MLP class
    classifier = MLP(rng=rng, input=x, n_in=dataset.n_in,
                     n_hidden=hyper.nHidden1, n_out=dataset.n_out)

    # the cost we minimize during training is the negative log likelihood of
    # the model plus the regularization terms (L1 and L2); cost is expressed
    # here symbolically
    cost = classifier.negative_log_likelihood(y) \
         + hyper.L1Reg * classifier.L1 \
         + hyper.L2Reg * classifier.L2_sqr

    # compiling a Theano function that computes the mistakes that are made
    # by the model on a minibatch
    test_model = theano.function(inputs=[index],
            outputs=classifier.errors(y),
            givens={
                x: test_set_x[index * hyper.batchSize:(index + 1) * hyper.batchSize],
                y: test_set_y[index * hyper.batchSize:(index + 1) * hyper.batchSize]})

    validate_model = theano.function(inputs=[index],
            outputs=classifier.errors(y),
            givens={
                x: valid_set_x[index * hyper.batchSize:(index + 1) * hyper.batchSize],
                y: valid_set_y[index * hyper.batchSize:(index + 1) * hyper.batchSize]})

    # compute the gradient of cost with respect to theta (sotred in params)
    # the resulting gradients will be stored in a list gparams
    gparams = []
    for param in classifier.params:
        gparam = T.grad(cost, param)
        gparams.append(gparam)

    # specify how to update the parameters of the model as a list of
    # (variable, update expression) pairs
    updates = []
    # given two list the zip A = [a1, a2, a3, a4] and B = [b1, b2, b3, b4] of
    # same length, zip generates a list C of same size, where each element
    # is a pair formed from the two lists :
    #    C = [(a1, b1), (a2, b2), (a3, b3), (a4, b4)]
    for param, gparam in zip(classifier.params, gparams):
        updates.append((param, param - hyper.learningRate * gparam))

    # compiling a Theano function `train_model` that returns the cost, but
    # in the same time updates the parameter of the model based on the rules
    # defined in `updates`
    train_model = theano.function(inputs=[index], outputs=cost,
            updates=updates,
            givens={
                x: train_set_x[index * hyper.batchSize:(index + 1) * hyper.batchSize],
                y: train_set_y[index * hyper.batchSize:(index + 1) * hyper.batchSize]})

    ###############
    # TRAIN MODEL #
    ###############
    print '... training'

    best_params = None
    best_validation_loss = numpy.inf
    best_iter = 0
    test_score = 0.
    start_time = time.clock()

    epoch = 0
    done_looping = False
    patience = hyper.patience

    while (epoch < hyper.numberEpochs) and (not done_looping):
        epoch = epoch + 1
        print('epoch %i, time %0.2fm' % (epoch, (time.clock() - start_time) / 60.0))
        for minibatch_index in xrange(n_train_batches):

            minibatch_avg_cost = train_model(minibatch_index)
            # iteration number
            iter = (epoch - 1) * n_train_batches + minibatch_index

            if (iter + 1) % validationFrequency == 0:
                # compute zero-one loss on validation set
                validation_losses = [validate_model(i) for i
                                     in xrange(n_valid_batches)]
                this_validation_loss = numpy.mean(validation_losses)

                print('epoch %i, minibatch %i/%i, validation error %f %%' %
                     (epoch, minibatch_index + 1, n_train_batches,
                      this_validation_loss * 100.))

                # if we got the best validation score until now
                if this_validation_loss < best_validation_loss:
                    #improve patience if loss improvement is good enough
                    if this_validation_loss < best_validation_loss *  \
                           hyper.improvementThreshold:
                        patience = max(patience, iter * hyper.patienceIncrease)

                    best_validation_loss = this_validation_loss
                    best_iter = iter

                    # test it on the test set
                    test_losses = [test_model(i) for i
                                   in xrange(n_test_batches)]
                    test_score = numpy.mean(test_losses)

                    print(('     epoch %i, minibatch %i/%i, test error of '
                           'best model %f %%') %
                          (epoch, minibatch_index + 1, n_train_batches,
                           test_score * 100.))

            if patience <= iter:
                    done_looping = True
                    break

    end_time = time.clock()
    print(('Optimization complete. Best validation score of %f %% '
           'obtained at iteration %i, with test performance %f %%') %
          (best_validation_loss * 100., best_iter + 1, test_score * 100.))
    print >> sys.stderr, ('The code for file ' +
                          os.path.split(__file__)[1] +
                          ' ran for %.2fm' % ((end_time - start_time) / 60.))


if __name__ == '__main__':
    #test_mlp(ds.CifarFeatures(ds.Cifar10Part()), HyperparametersMLP(numberEpochs=1000))
    test_mlp(ds.Mnist(), HyperparametersMLP(numberEpochs=10))
