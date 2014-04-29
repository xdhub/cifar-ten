"""
"""
import cPickle
import gzip
import os
import sys
import time

import numpy

import theano
import theano.tensor as T
from theano.tensor.shared_randomstreams import RandomStreams

import cifarDirectories
sys.path.append(cifarDirectories.DeepLearningTutorialsCode())
from DBN import DBN

import dataset as ds
from hyperparameter import HyperparametersDBN

def test_DBN(dataset, hyper):
    datasets = dataset.sharedTrain, dataset.sharedValid, dataset.sharedTest

    train_set_x, train_set_y = dataset.sharedTrain
    valid_set_x, valid_set_y = dataset.sharedValid
    test_set_x, test_set_y = dataset.sharedTest

    n_train_batches = train_set_x.get_value(borrow=True).shape[0] / hyper.batchSize

    # numpy random generator
    numpy_rng = numpy.random.RandomState(123)
    print '... building the model'
    # construct the Deep Belief Network
    dbn = DBN(numpy_rng=numpy_rng, n_ins=dataset.n_in,
              hidden_layers_sizes=[1000, 1000, 1000],
              n_outs=dataset.n_out)

    #########################
    # PRETRAINING THE MODEL #
    #########################
    print '... getting the pretraining functions'
    pretraining_fns = dbn.pretraining_functions(train_set_x=train_set_x,
                                                batch_size=hyper.batchSize,
                                                k=hyper.k)

    print '... pre-training the model'
    start_time = time.clock()
    ## Pre-train layer-wise
    for i in xrange(dbn.n_layers):
        # go through pretraining epochs
        for epoch in xrange(hyper.pretrainingEpochs):
            # go through the training set
            c = []
            for batch_index in xrange(n_train_batches):
                c.append(pretraining_fns[i](index=batch_index,
                                            lr=hyper.pretrainingLearningRate))
            print 'Pre-training layer %i, epoch %d, cost ' % (i, epoch),
            print numpy.mean(c)

    end_time = time.clock()
    print >> sys.stderr, ('The pretraining code for file ' +
                          os.path.split(__file__)[1] +
                          ' ran for %.2fm' % ((end_time - start_time) / 60.))

    print '... getting the finetuning functions'
    train_fn, validate_model, test_model = dbn.build_finetune_functions(
                datasets=datasets, batch_size=hyper.batchSize,
                learning_rate=hyper.learningRate)

    print '... finetunning the model'
    # early-stopping parameters
    patience = 4 * n_train_batches  # look as this many examples regardless
    validation_frequency = min(n_train_batches, patience / 2)

    best_params = None
    best_validation_loss = numpy.inf
    test_score = 0.
    start_time = time.clock()

    done_looping = False
    epoch = 0

    while (epoch < hyper.numberEpochs) and (not done_looping):
        epoch = epoch + 1
        for minibatch_index in xrange(n_train_batches):

            minibatch_avg_cost = train_fn(minibatch_index)
            iter = (epoch - 1) * n_train_batches + minibatch_index

            if (iter + 1) % validation_frequency == 0:

                validation_losses = validate_model()
                this_validation_loss = numpy.mean(validation_losses)
                print('epoch %i, minibatch %i/%i, validation error %f %%' % \
                      (epoch, minibatch_index + 1, n_train_batches,
                       this_validation_loss * 100.))

                # if we got the best validation score until now
                if this_validation_loss < best_validation_loss:

                    #improve patience if loss improvement is good enough
                    if (this_validation_loss < best_validation_loss *
                        hyper.improvementThreshold):
                        patience = max(patience, iter * hyper.patienceIncrease)

                    # save best validation score and iteration number
                    best_validation_loss = this_validation_loss
                    best_iter = iter

                    # test it on the test set
                    test_losses = test_model()
                    test_score = numpy.mean(test_losses)
                    print(('     epoch %i, minibatch %i/%i, test error of '
                           'best model %f %%') %
                          (epoch, minibatch_index + 1, n_train_batches,
                           test_score * 100.))

            if patience <= iter:
                done_looping = True
                break

    end_time = time.clock()
    print(('Optimization complete with best validation score of %f %%,'
           'with test performance %f %%') %
                 (best_validation_loss * 100., test_score * 100.))
    print >> sys.stderr, ('The fine tuning code for file ' +
                          os.path.split(__file__)[1] +
                          ' ran for %.2fm' % ((end_time - start_time)
                                              / 60.))


if __name__ == '__main__':
    #test_DBN(ds.Mnist(), HyperparametersDBN(numberEpochs = 10, pretrainingEpochs = 1))
    test_DBN(ds.CifarFeatures(ds.Cifar10Part()), HyperparametersDBN(pretrainingEpochs = 100, numberEpochs=1000))

