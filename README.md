cifar-ten
=========

Studio 415 ml meetup.

Download the data
-----------------

The bash script `grabData.sh` will create a directory `data` and subdirectories to contain the MNIST, CIFAR-10 and CIFAR-100 datasets.

The python scripts in the `code` directory expect these directories to exist, as well as an additional directory, `data/cifarKaggle`, which must be populated by hand using the data from Kaggle.com. Expected files and subdirectories are
  * `data/cifarKaggle/trainLabels.csv` from [http://www.kaggle.com/c/cifar-10/download/trainLabels.csv](http://www.kaggle.com/c/cifar-10/download/trainLabels.csv)
  * `data/cifarKaggle/train` the unzipped contents of [http://www.kaggle.com/c/cifar-10/download/train.7z](http://www.kaggle.com/c/cifar-10/download/train.7z)
  * `data/cifarKaggle/test` the unzipped contents of [http://www.kaggle.com/c/cifar-10/download/test.7z](http://www.kaggle.com/c/cifar-10/download/test.7z)

If the python script in the `code` directory are not run from the code directory, then they will expect expect that environment variable `HOME` be set. In that case, they will look for python scripts in directory `$HOME/cifar-ten/code/` and data files in subdirectories of `$HOME/cifar-ten/data`.

Required python packages
------------------------

Currently the python scripts in `code` require packages numpy, scipy, Theano and PyWavelets. To install these packages system-wide, invoke
  * `sudo pip install Theano`
  * `sudo pip install PyWavelets`

If local installation is sufficient or preferred, invoke `pip` with the `--user` flag. 

