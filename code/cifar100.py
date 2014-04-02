import cifarDirectories
import os
import tarfile
import cPickle

def getData(filename):
    path = os.path.join(cifarDirectories.data(), 'cifar-100-python.tar.gz')
    f = tarfile.open(path, 'r:gz')
    data = cPickle.load(f.extractfile(filename))
    f.close()
    return data

def train():
    return getData('cifar-100-python/train')
    
def test():
    return getData('cifar-100-python/test')
    
def meta():
    return getData('cifar-100-python/meta')
    
