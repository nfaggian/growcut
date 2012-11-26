""" Python implementation of growcut """

import numpy as np

from scipy import ndimage
from scipy import misc


NEIGHBOURS = [(-1, 0), (1, 0), (0, 1), (0, -1)]


def iterNeighbours((r, c), neighbours=NEIGHBOURS):
    """ Yield the point neighborhood """

    for (dx, dy) in neighbours:
        yield (r + dx, c + dy)


# Numpy approach.
def vonNeumannSampler(shape):
    sr = []
    sc = []
    for (r, c) in np.ndindex(shape):
        sr.append([r-1, r+1, r, r])
        sc.append([c, c, c+1, c-1])
    return np.array(sr), np.array(sc)

