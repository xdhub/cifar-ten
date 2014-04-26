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

function cloneRepos()
{
    pushd .
    cd demos
    
    git clone git@github.com:lisa-lab/DeepLearningTutorials.git
    git clone git@github.com:fsprojects/Vulpes.git
    git clone git@github.com:jdeng/rbm-mnist.git
    svn checkout http://cuda-convnet.googlecode.com/svn/trunk/ cuda-convnet-read-only
    
    popd
}

createDirectories
downloadFiles
cloneRepos

