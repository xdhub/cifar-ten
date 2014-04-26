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

    pushd .
    cd data

    if [ -e mnist.pkl.gz ]
    then
        echo MNIST data set already downloaded.
    else
        curl http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz > mnist.pkl.gz
    fi

    if [ -e cifar-10-python.tar.gz ]
    then
        echo CIFAR 10 data set already downloaded.
    else
        curl http://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz > cifar-10-python.tar.gz
    fi
    
    if [ -e cifar-100-python.tar.gz ]
    then
        echo CIFAR 100 data set already downloaded.
    else
        curl http://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz > cifar-100-python.tar.gz
    fi
    
    popd
}

function cloneRepos()
{
    pushd .
    cd demos
    
    git clone git@github.com:lisa-lab/DeepLearningTutorials.git
    git clone git@github.com:fsprojects/Vulpes.git
    git clone git@github.com:jdeng/rbm-mnist.git
    git clone git@github.com:nigma/pywt.git

    if [ -e cuda-convnet-read-only ]
    then
        echo cuda-convnet repo set already cloned.
    else
        svn checkout http://cuda-convnet.googlecode.com/svn/trunk/ cuda-convnet-read-only
    fi
    
    popd
}

createDirectories
downloadFiles
cloneRepos

