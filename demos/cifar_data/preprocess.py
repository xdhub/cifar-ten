import numpy
from numpy import fft
from PIL import Image
import pywt
import os

def load(name):
    # don't want name to be a number or any data type other than string
    name = str(name)
    # construct the path assuming the environment variable is set to the location
    # of the CIFAR-10 data directory, which has a subdirectory train
    path = os.path.join(os.environ['CIFIR_DATA_DIR'], 'train', str(name) + '.png')
    return Image.open(path)

def normalize(image):
    # find the dimensions of image, which is assumed to be square
    n = image.size[0]
    
    # construct a list of three arrays, one for each channel RGB, RGBA, etc.
    arr = [numpy.fromstring(i.tostring(), numpy.uint8) for i in image.split()]
    
    # mean normalize the arrays
    flat = numpy.concatenate(arr)
    mu = flat.mean()
    sigma = flat.std()
    arr = [(a - mu)/sigma for a in arr]
    
    # reshape the arrays to square arrays and return the results
    return [numpy.reshape(a, (n, n)) for a in arr]    

def conflatten(arr):
    return numpy.concatenate([a.flatten() for a in arr])

def conflattenDwt(a):
    dw = pywt.dwt2(a, 'db3', 'sym')
    b = conflatten(dw[1])
    return conflatten([dw[0], b])

def loadImageFeatures(name):
    image = load(name)
    # find the dimensions of image, which is assumed to be square
    n = image.size[0]

    arr = normalize(image)
    
    # compute the 2d Fourier transform of each channel and flatten into features
    f = conflatten([abs(fft.fft2(a)) / (n * n) for a in arr])
    
    # compute a wavelet transform of the channels
    # flatten the results to get features
    dw = conflatten([conflattenDwt(a) for a in arr])
    
    return numpy.concatenate([dw, f])

