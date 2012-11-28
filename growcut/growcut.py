""" Implementation of the grow-cut algorithm """

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

    nextLabel = label.copy()
    nextStrength = strength.copy()

    for point, (neighbourLum, neighbourStrength, neigbourLabel) in automata.iterGrids(
        (lum, strength, label), neighbours=automata.CONNECT_8
        ):

        cp = lum[point]
        thetap = strength[point]

        C = np.array(neighbourLum)

        for cq, thetaq, lq in zip(neighbourLum, neighbourStrength, neigbourLabel):

            if g(norm(cp - cq), C) * thetaq > thetap:
                nextLabel[point] = lq
                nextStrength[point] = g(norm(cp - cq), C) * thetaq

    return nextStrength, nextLabel
