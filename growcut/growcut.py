""" Implementation of the grow-cut algorithm """

import numpy as np

np.set_printoptions(threshold=100000)

import automata


def g(x, maxC):
    """ Damping function """
    return 1. - ((x * 1.) / maxC)


def norm(x):
    """ L2 norm """
    #return np.sqrt(np.sum(np.power(x, 2)))
    return np.linalg.norm(x)


def numpyAutomate(lum, strength, label):
    """ Numpy based grow-cut """

    nextLabel = label.copy().flatten()
    nextStrength = strength.copy().flatten()
    coordinates = automata.formSamples(lum.shape, neighbours=automata.CONNECT_4)

    CP = lum.flatten()
    THETAP = strength.flatten()

    CQ = automata.sample(lum, coordinates)
    THETAQ = automata.sample(strength, coordinates)
    LQ = automata.sample(label, coordinates)

    CPminusCQ = np.vstack([CP] * CQ.shape[1]).T - CQ

    attackStrength = g(CPminusCQ, lum.max()) * THETAQ
    defendStrength = np.vstack([THETAP] * CQ.shape[1]).T

    c = np.argmax(attackStrength > defendStrength, axis=1)
    r = np.arange(0, attackStrength.shape[0])
    mask = np.alltrue(~(attackStrength > defendStrength), axis=1)

    # Fill the new strengths
    nextLabel[mask] = LQ[r[mask], c[mask]]
    nextStrength[mask] = attackStrength[r[mask], c[mask]]

    return nextStrength.reshape(strength.shape), nextLabel.reshape(label.shape)


def automate(lum, strength, label):
    """ Grow-cut """

    nextLabel = label.copy()
    nextStrength = strength.copy()

    for point, (neighbourLum, neighbourStrength, neigbourLabel) in automata.iterGrids(
        (lum, strength, label), neighbours=automata.CONNECT_4
        ):

        cp = lum[point]
        thetap = strength[point]

        for cq, thetaq, lq in zip(neighbourLum, neighbourStrength, neigbourLabel):

            if g(norm(cp - cq), lum.max()) * thetaq > thetap:
                nextLabel[point] = lq
                nextStrength[point] = g(norm(cp - cq), lum.max()) * thetaq

    return nextStrength, nextLabel
