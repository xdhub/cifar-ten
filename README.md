cifar-ten
=========

Studio 415 ml meetup.

Download the data
-----------------

The bash script `grabDependencies.sh` will download data and clone several repositories that contain examples and dependencies. It will create a directory `data` and subdirectories to contain the MNIST, CIFAR-10 and CIFAR-100 datasets.

The python scripts in the `code` directory expect these directories to exist, as well as an additional directory, `data/cifarKaggle`, which must be populated by hand using the data from Kaggle.com. Expected files and subdirectories are
  * `data/cifarKaggle/trainLabels.csv` from [http://www.kaggle.com/c/cifar-10/download/trainLabels.csv](http://www.kaggle.com/c/cifar-10/download/trainLabels.csv)
  * `data/cifarKaggle/train` the unzipped contents of [http://www.kaggle.com/c/cifar-10/download/train.7z](http://www.kaggle.com/c/cifar-10/download/train.7z)
  * `data/cifarKaggle/test` the unzipped contents of [http://www.kaggle.com/c/cifar-10/download/test.7z](http://www.kaggle.com/c/cifar-10/download/test.7z)

The python scripts in the `code` directory will try to identify the location of the `cifar-ten` directory. First they will check if there is an environment variable `CIFAR10_HOME`, in which case they will assume that is the location of the `cifar-ten` directory. If that environment variable is not set, then it will look for python scripts in directory `$HOME/cifar-ten/code/` and data files in subdirectories of `$HOME/cifar-ten/data`.

Required python packages
------------------------

Currently the python scripts in `code` require packages numpy, scipy, Theano and PyWavelets. To install these packages system-wide, invoke
  * `sudo pip install Theano`
  * `sudo pip install PyWavelets`

If local installation is sufficient or preferred, invoke `pip` with the `--user` flag. 

