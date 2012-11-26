""" Tests for the automata module """

from growcut import automata

import numpy as np


def test_neighbours():
    """ Assert the pattern of the neighbourhood is correct """

    point = (10, 10)
    pointIterator = automata.iterNeighbours(point)

    assert np.allclose(pointIterator.next(), (9, 10))
    assert np.allclose(pointIterator.next(), (11, 10))
    assert np.allclose(pointIterator.next(), (10, 11))
    assert np.allclose(pointIterator.next(), (10, 9))


def test_iterGrid():
    """ Assert the correct pattern of samples """

    rows, cols = np.mgrid[0:10, 0:10]

    automata.iterGrid(rows)

    assert False
