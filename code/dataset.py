import numpy

import theano
import theano.tensor as T

import cifar10
import mnist

class Dataset(object):
    def __init__(self, train, valid, test):
        self.train = train
        self.valid = valid
        self.test = test
        self.initN()
        self.initSharedData()

    def initSharedData(self):
        def sharedPair(data):
            def shared(z):
                return theano.shared(numpy.asarray(z, dtype=theano.config.floatX), borrow=True) 
                
            x, y = data
            return shared(x), T.cast(shared(y), 'int32')
            
        self.sharedTrain = sharedPair(self.train)
        self.sharedValid = sharedPair(self.valid)
        self.sharedTest = sharedPair(self.test)
        
    def initN(self):
        self.n_in = len(self.train[0][0])
        self.n_out = max(self.train[1]) + 1
        
class Cifar10Part(Dataset):
    def __init__(self):
        batch = cifar10.batch1()
        train = batch['data'], batch['labels']
        batch = cifar10.batch2()
        valid = batch['data'], batch['labels']
        batch = cifar10.batch3()
        test = batch['data'], batch['labels']
        Dataset.__init__(self, train, valid, test)

class CifarFeatures(Dataset):
    def __init__(self, cifarDataset):
        def transform(data):
            from preprocess import dwtFftFeatures as feat
            from preprocess import reconstruct as recon
            x, y = data
            z = [feat(recon(a, (32, 32))) for a in x]
            return z, y
            
        train = transform(cifarDataset.train)
        valid = transform(cifarDataset.valid)
        test = transform(cifarDataset.test)
        Dataset.__init__(self, train, valid, test)
    
class Mnist(Dataset):
    def __init__(self):
        train, valid, test = mnist.mnist()
        Dataset.__init__(self, train, valid, test)

