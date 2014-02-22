"""Load images in a format that can be passed to scikit learn

load() function is what you are looking for. See its docstring for details.

"""

import csv
import os
import numpy as np

import npimage


class ImageList(object):

    """List of cifar images.

    Naming convention:
    iid - image id
    lid - lable id
    lname - label name

    """

    def __init__(self, data_dir):
        self.iid_lid = []
        self.lnames = []
        self._csv_fpath = os.path.join(data_dir, "trainLabels.csv")
        self._img_fpath_format = os.path.join(data_dir, "train", "%s.png")
        self._load()

    def _load(self):
        iid_lname = [(row[0], row[1]) for row in csv.reader(open(self._csv_fpath, "rb")) if row[0] != "id"]
        self.lnames = list(set([lname for iid, lname in iid_lname]))
        self.lnames.sort()
        self.iid_lid = [(iid, self.lid_from_lname(label)) for iid, label in iid_lname]

    def fpath_from_iid(self, iid):
        return self._img_fpath_format % (iid,)

    def lid_from_lname(self, lname):
        return self.lnames.index(lname)

    def lname_from_lid(self, lid):
        return self.lnames[lid]


def load(n_samples, lnames=None):
    """Load n_sample images from the test set.

    Set environment variable CIFIR_DATA_DIR to point to the directory
    with cifar data. It needs to have trainLabels.csv file and a subdir
    "train" with PNG images.

    :param n_samples: number of samples to load
    :param lnames: optional list of sample labels
    :returns: Bunch object from scikit learn, populated with samples according
    to the scikit learn convention, with data, target and target_names fields.

    >>> samples = load(50, ("airplane", "automobile"))
    >>> print samples.keys()
    ['data', 'target', 'target_names']
    >>> print samples.data.shape
    (50, 3072)
    >>> print samples.target.shape
    (50,)

    """
    assert lnames is None or isinstance(lnames, (list, tuple))

    try:
        cifar_data_dir = os.environ["CIFIR_DATA_DIR"]
    except KeyError:
        import sys
        sys.stderr.write("Set CIFIR_DATA_DIR environment variable to the directory with trainLabels.csv and train/*.png\n")
        sys.exit(1)

    il = ImageList(cifar_data_dir)

    if not lnames:
        lnames = il.lnames

    filter_lids = [il.lid_from_lname(lname) for lname in lnames]
    iid_lid = [(iid, lid) for iid, lid in il.iid_lid if lid in filter_lids][:n_samples]
    image_paths = [il.fpath_from_iid(iid) for iid, lid in iid_lid]
    data = np.vstack([npimage.flatten(npimage.load(ipath)) for ipath in image_paths])
    target = np.array([lid for iid, lid in iid_lid])

    from sklearn.datasets.base import Bunch
    return Bunch(data=data, target=target, target_names=il.lnames)
