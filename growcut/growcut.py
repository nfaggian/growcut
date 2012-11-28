""" Implementation of the grow cut algorithm

V. Vezhnevets, V. Konouchine (2005).
    "Grow-Cut" - Interactive Multi-Label N-D Image Segmentation".
        Proc. Graphicon. pp. 150–156.
"""

import numpy as np

import automata


def g(x, C):
    """ Damping function """
    return 1. - (float(x) / float(max(C)))


def norm(x):
    """ L2 norm """
    #return np.sqrt(np.sum(np.power(x, 2)))
    return np.linalg.norm(x)


def automate(lum, strength, label):
    """ Grow-cut """

    nextLabel = np.zeros_like(label)

    for point, (lumValues, strengthValues, labelValues) in iterGrid(state, neighbours=CONNECT_8):
      pass

    return nextLabel

