#!/bin/bash

function createDirectories()
{
    echo Creating data directories.

    mkdir data
    mkdir data/cifarKaggle
    mkdir data/cifarKaggle/test
    mkdir data/cifarKaggle/train
}

function downloadFiles()
{
    echo Downloading data.

    curl http://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz > data/cifar-10-python.tar.gz
    curl http://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz > data/cifar-100-python.tar.gz
    curl http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz > data/mnist.pkl.gz
}

createDirectories
downloadFiles

