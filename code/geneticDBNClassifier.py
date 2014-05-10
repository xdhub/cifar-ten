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

import dataset
from hyperparameter import HyperparametersDBN

def test_DBN(dataset, hyper):
    datasets = dataset.sharedTrain, dataset.sharedValid, dataset.sharedTest

    train_set_x, train_set_y = dataset.sharedTrain
    valid_set_x, valid_set_y = dataset.sharedValid
    test_set_x, test_set_y = dataset.sharedTest

    n_train_batches = train_set_x.get_value(borrow=True).shape[0] / hyper.batchSize

    numpy_rng = numpy.random.RandomState(123)
    print '... building the model'

    dbn = DBN(numpy_rng=numpy_rng, n_ins=dataset.n_in,
              hidden_layers_sizes=hyper.nHidden,
              n_outs=dataset.n_out)

    print '... getting the pretraining functions'
    pretraining_fns = dbn.pretraining_functions(train_set_x=train_set_x,
                                                batch_size=hyper.batchSize,
                                                k=hyper.k)

    # Start timeout timer
    wait_timeout(test_DBN, 30)

    print '... pre-training the model'
    start_time = time.time()

    for i in xrange(dbn.n_layers):
        for epoch in xrange(hyper.pretrainingEpochs):
            print "Pretraining epoch ", epoch, ", time ", (time.time() - start_time) / 60.0
            c = []
            for batch_index in xrange(n_train_batches):
                c.append(pretraining_fns[i](index=batch_index,
                                            lr=hyper.pretrainingLearningRate))
            print 'Pre-training layer %i, epoch %d, cost ' % (i, epoch),
            print numpy.mean(c)

    end_time = time.time()
    print('The pretraining code for file ' +
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
    start_time = time.time()

    done_looping = False
    epoch = 0

    while (epoch < hyper.numberEpochs) and (not done_looping):
        epoch = epoch + 1
	print "Finetuning epoch ", epoch, ", time ", (time.time() - start_time) / 60.0 
        for minibatch_index in xrange(n_train_batches):

            minibatch_avg_cost = train_fn(minibatch_index)
            iter = (epoch - 1) * n_train_batches + minibatch_index

            if (iter + 1) % validation_frequency == 0:

                validation_losses = validate_model()
                this_validation_loss = numpy.mean(validation_losses)
                print('epoch %i, minibatch %i/%i, validation error %f %%' % \
                      (epoch, minibatch_index + 1, n_train_batches,
                       this_validation_loss * 100.))

                if this_validation_loss < best_validation_loss:

                    if (this_validation_loss < best_validation_loss *
                        hyper.improvementThreshold):
                        patience = max(patience, iter * hyper.patienceIncrease)

                    best_validation_loss = this_validation_loss
                    best_iter = iter

                    test_losses = test_model()
                    test_score = numpy.mean(test_losses)
                    print(('     epoch %i, minibatch %i/%i, test error of '
                           'best model %f %%') %
                          (epoch, minibatch_index + 1, n_train_batches,
                           test_score * 100.))

            if patience <= iter:
                done_looping = True
                break

    end_time = time.time()
    print(('Optimization complete with best validation score of %f %%,'
           'with test performance %f %%') %
                 (best_validation_loss * 100., test_score * 100.))
    print('The fine tuning code for file ' +
                          os.path.split(__file__)[1] +
                          ' ran for %.2fm' % ((end_time - start_time)
                                              / 60.))


def wait_timeout(proc, minutes):
    # Wait for a process to finish, or kill process after timeout
    start = time.time()
    end = start + (minutes * 60)

    while True:
        if time.time() >= end:
            raise RuntimeError("Process took greater than %i minutes" % (minutes))
	    os.kill(pid, signal.SIGKILL)
            killedpid, stat = os.waitpid(pid, os.WNOHANG)
            if killedpid == 0:
		print >> sys.stderr, "PROCESS WAS NOT KILLED"



if __name__ == '__main__':
    test_DBN(dataset.Mnist(), HyperparametersDBN(numberEpochs = 10, pretrainingEpochs = 2))
    #test_DBN(dataset.Mnist(), HyperparametersDBN(numberEpochs = 100, pretrainingEpochs = 10, nHidden=[5000, 5000, 5000]))
    #test_DBN(dataset.CifarFeatures(dataset.Cifar10Part()), HyperparametersDBN(pretrainingEpochs = 100, numberEpochs=1000, nHidden=[5000, 5000, 5000]))

