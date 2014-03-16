#!/bin/bash

function createDirectories()
{
    echo Creating data directories.

    mkdir data
    mkdir data/mnist
    mkdir data/cifar10
    mkdir data/cifar100
}

function downloadFiles()
{
    echo Downloading data.

    curl http://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz > data/cifar10/cifar-10-python.tar.gz
    curl http://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz > data/cifar100/cifar-100-python.tar.gz
    curl http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz > data/mnist/train-images-idx3-ubyte.gz
    curl http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz > data/mnist/train-labels-idx1-ubyte.gz
    curl http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz > data/mnist/t10k-images-idx3-ubyte.gz
    curl http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz > data/mnist/t10k-labels-idx1-ubyte.gz
}

function unzipFiles()
{
    echo Unzipping data.

    pushd .
    cd data/cifar10/
    gzip -dv < cifar-10-python.tar.gz | tar xvf - 
    popd
    pushd .
    cd data/cifar100/
    gzip -dv < cifar-100-python.tar.gz | tar xvf -
    popd
    
    gzip -dv data/mnist/train-images-idx3-ubyte.gz
    gzip -dv data/mnist/train-labels-idx1-ubyte.gz
    gzip -dv data/mnist/t10k-images-idx3-ubyte.gz
    gzip -dv data/mnist/t10k-labels-idx1-ubyte.gz
}

createDirectories
downloadFiles
unzipFiles

