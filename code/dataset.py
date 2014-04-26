import numpy

import theano
import theano.tensor as T

import cifar10
import mnist

class Dataset(object):
    def __init__(self):
        self.n_in = 0
        self.n_out = 0
        self.n_channels = 0

    def shared_dataset(self, data_xy, borrow=True):
        data_x, data_y = data_xy
        shared_x = theano.shared(numpy.asarray(data_x,
                                               dtype=theano.config.floatX),
                                 borrow=borrow)
        shared_y = theano.shared(numpy.asarray(data_y,
                                               dtype=theano.config.floatX),
                                 borrow=borrow)
        return shared_x, T.cast(shared_y, 'int32')

    def loadData(self):
        train_set_x, train_set_y = self.shared_dataset(self.trainingSet)
        valid_set_x, valid_set_y = self.shared_dataset(self.validationSet)
        test_set_x, test_set_y = self.shared_dataset(self.testSet)

        rval = [(train_set_x, train_set_y), (valid_set_x, valid_set_y),
                (test_set_x, test_set_y)]
        return rval

class Cifar10Part(Dataset):
    def __init__(self):
        Dataset.__init__(self)
        self.n_in = 32 * 32 * 3
        self.n_out = 10
        self.n_channels = 1
        data = cifar10.batch1()
        self.trainingSet = (data['data'], data['labels'])
        data = cifar10.batch2()
        self.validationSet = (data['data'], data['labels'])
        data = cifar10.batch3()
        self.testSet = (data['data'], data['labels'])

class CifarFeatures(Dataset):
    def __init__(self, cifarDataset):
        Dataset.__init__(self)

        def transform(data):
            from preprocess import dwtFftFeatures as feat
            from preprocess import reconstruct as recon
            x, y = data
            z = [feat(recon(a, (32, 32))) for a in x]
            return (z, y)

        self.trainingSet = transform(cifarDataset.trainingSet)
        self.validationSet = transform(cifarDataset.validationSet)
        self.testSet = transform(cifarDataset.testSet)

        self.n_in = len(self.trainingSet[0][0])
        self.n_out = cifarDataset.n_out
        self.n_channels = 1
    
class Mnist(Dataset):
    def __init__(self):
        Dataset.__init__(self)
        self.n_in = 28 * 28
        self.n_out = 10
        self.n_channels = 1
        self.trainingSet, self.validationSet, self.testSet = mnist.mnist()

