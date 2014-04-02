import cifarDirectories
import os
import gzip
import cPickle

def mnist():
    path = os.path.join(cifarDirectories.data(), 'mnist.pkl.gz')
    f = gzip.open(path, 'rb')
    data = cPickle.load(f)
    f.close()
    return data

