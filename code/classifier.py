import os
import sys
import time
import numpy

import theano
import theano.tensor as T

import cifarDirectories
sys.path.append(cifarDirectories.DeepLearningTutorialsCode())

import logistic_sgd

import dataset

class Classifier(object):
    def __init__(self):
        pass

class LogisticRegression(Classifier, logistic_sgd.LogisticRegression):
    def __init__(self, input, dataset):
        logistic_sgd.LogisticRegression.__init__(self, input, dataset.n_in, dataset.n_out)

class HyperParameters(object):
    def __init__(self, learningRate=0.13, numberEpochs=1000, batchSize=600, patience = 5000, patienceIncrease = 2, improvementThreshold = 0.995):
        self.learningRate = learningRate
        self.numberEpochs = numberEpochs
        self.batchSize = batchSize
        self.patience = patience
        self.patienceIncrease = patienceIncrease
        self.improvementThreshold = improvementThreshold

def sgd_optimization(dataset, hyper):
    print dataset.n_in, dataset.n_out

    train_set_x, train_set_y = dataset.sharedTrain
    valid_set_x, valid_set_y = dataset.sharedValid
    test_set_x, test_set_y = dataset.sharedTest

    n_train_batches = train_set_x.get_value(borrow=True).shape[0] / hyper.batchSize
    n_valid_batches = valid_set_x.get_value(borrow=True).shape[0] / hyper.batchSize
    n_test_batches = test_set_x.get_value(borrow=True).shape[0] / hyper.batchSize
    
    validationFrequency = min(n_train_batches, hyper.patience / 2)

    index = T.lscalar()  # index to a [mini]batch
    x = T.matrix('x')  # the data is presented as rasterized images
    y = T.ivector('y')  # the labels are presented as 1D vector of
                           # [int] labels

    classifier = LogisticRegression(input=x, dataset=dataset)
    cost = classifier.negative_log_likelihood(y)

    test_model = theano.function(inputs=[index],
            outputs=classifier.errors(y),
            givens={
                x: test_set_x[index * hyper.batchSize: (index + 1) * hyper.batchSize],
                y: test_set_y[index * hyper.batchSize: (index + 1) * hyper.batchSize]})

    validate_model = theano.function(inputs=[index],
            outputs=classifier.errors(y),
            givens={
                x: valid_set_x[index * hyper.batchSize:(index + 1) * hyper.batchSize],
                y: valid_set_y[index * hyper.batchSize:(index + 1) * hyper.batchSize]})

    gradW = T.grad(cost=cost, wrt=classifier.W)
    gradb = T.grad(cost=cost, wrt=classifier.b)

    updates = [(classifier.W, classifier.W - hyper.learningRate * gradW),
               (classifier.b, classifier.b - hyper.learningRate * gradb)]

    train_model = theano.function(inputs=[index],
            outputs=cost,
            updates=updates,
            givens={
                x: train_set_x[index * hyper.batchSize:(index + 1) * hyper.batchSize],
                y: train_set_y[index * hyper.batchSize:(index + 1) * hyper.batchSize]})

    best_params = None
    best_validation_loss = numpy.inf
    test_score = 0.
    start_time = time.clock()

    done_looping = False
    epoch = 0
    patience = hyper.patience
    while (epoch < hyper.numberEpochs) and (not done_looping):
        epoch = epoch + 1
        for minibatch_index in xrange(n_train_batches):

            minibatch_avg_cost = train_model(minibatch_index)
            # iteration number
            iter = (epoch - 1) * n_train_batches + minibatch_index

            if (iter + 1) % validationFrequency == 0:
                # compute zero-one loss on validation set
                validation_losses = [validate_model(i)
                                     for i in xrange(n_valid_batches)]
                this_validation_loss = numpy.mean(validation_losses)

                print('epoch %i, minibatch %i/%i, validation error %f %%' % \
                    (epoch, minibatch_index + 1, n_train_batches,
                    this_validation_loss * 100.))

                # if we got the best validation score until now
                if this_validation_loss < best_validation_loss:
                    #improve patience if loss improvement is good enough
                    if this_validation_loss < best_validation_loss *  \
                       hyper.improvementThreshold:
                        patience = max(patience, iter * hyper.patienceIncrease)

                    best_validation_loss = this_validation_loss
                    # test it on the test set

                    test_losses = [test_model(i)
                                   for i in xrange(n_test_batches)]
                    test_score = numpy.mean(test_losses)

                    print(('     epoch %i, minibatch %i/%i, test error of best'
                       ' model %f %%') %
                        (epoch, minibatch_index + 1, n_train_batches,
                         test_score * 100.))

            if patience <= iter:
                done_looping = True
                break

    end_time = time.clock()
    print(('Optimization complete with best validation score of %f %%,'
           'with test performance %f %%') %
                 (best_validation_loss * 100., test_score * 100.))
    print 'The code run for %d epochs, with %f epochs/sec' % (
        epoch, 1. * epoch / (end_time - start_time))
    print >> sys.stderr, ('The code for file ' +
                          os.path.split(__file__)[1] +
                          ' ran for %.1fs' % ((end_time - start_time)))

if __name__ == '__main__':
    sgd_optimization(dataset.Mnist(), HyperParameters())

