import cifarDirectories
import os
import tarfile
import cPickle

def getData(filename):
    path = os.path.join(cifarDirectories.data(), 'cifar-10-python.tar.gz')
    f = tarfile.open(path, 'r:gz')
    data = cPickle.load(f.extractfile(filename))
    f.close()
    return data

def test():
    return getData('cifar-10-batches-py/test_batch')
    
def batch1():
    return getData('cifar-10-batches-py/data_batch_1')
    
def batch2():
    return getData('cifar-10-batches-py/data_batch_2')
    
def batch3():
    return getData('cifar-10-batches-py/data_batch_3')
    
def batch4():
    return getData('cifar-10-batches-py/data_batch_4')
    
def batch5():
    return getData('cifar-10-batches-py/data_batch_5')
    
def meta():
    return getData('cifar-10-batches-py/batches.meta')
    
