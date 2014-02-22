"""Convenience functions for manipulating images as numpy ndarrays

Naming convention
img3d - 3d (N,  M, 3) array. [n, m, :] are (r, g, b) values for pixel (n, m).
img1d - 1d (N*M*3,) array. All reds, followed by all greens, then blues.

flatten(): img3d -> img1d
unflatten(): img1d -> img3d

Flattened images is what we use for all learning functions.

Example:
>>> show(load("1.png"))


"""

import math
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def load(fpath):
    """Load an image ndarray (N, M, 3) from a png file."""
    img3d =  mpimg.imread(fpath)
    assert len(img3d.shape) == 3
    assert img3d.shape[2] in (3, 4) # RGB or RGBA

    # TODO: For now, just throw away the alpha channel.
    if img3d.shape[2] == 4:
        img3d = img3d.swapaxes(0, 2)[0:3].swapaxes(0, 2)
    assert img3d.shape[2] == 3
    return img3d


def save(fpath, img3d):
    """Save an image (N, M, 3) to a file.
    
    :TODO: matplotlib.pyplot.imsave saves as RGBA instead of RGB.

    """
    plt.imsave(fpath, img3d)


def show(img3d):
    """Display a image.
    
    :TODO: This will display an image scaled up. Need display as original size

    """
    plt.imshow(img3d)
    plt.show()


def flatten(img3d):
    """Flatten an image (N, M, 3) -> (N*M*3,)."""
    return img3d.swapaxes(0, 1).swapaxes(0, 2).flatten()


def unflatten(img1d):
    """Unflatten an image (N*N*3,) -> (NxNx3).

    Assumes the image is square.

    """
    assert len(img1d.shape) == 1
    size = int(math.sqrt(img1d.shape[0] / 3))
    assert size * size * 3 == img1d.shape[0]
    img3d = img1d.reshape(3, size, size).swapaxes(0, 2).swapaxes(0, 1)
    return img3d
