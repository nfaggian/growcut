""" Tests for the automata module """

from growcut import automata

import numpy as np


def test_neighbours():
    """ Assert the pattern of the neighborhood is correct """

    point = (5, 5)
    pointIterator = automata.iterNeighbours(point, (10, 10), automata.CONNECT_4)

    assert np.allclose(pointIterator.next(), (4, 5))
    assert np.allclose(pointIterator.next(), (6, 5))
    assert np.allclose(pointIterator.next(), (5, 6))
    assert np.allclose(pointIterator.next(), (5, 4))


def test_neighbours_origin():
    """ Assert the pattern of the neighborhood is correct """

    point = (0, 0)
    pointIterator = automata.iterNeighbours(point, (10, 10), automata.CONNECT_4)

    assert np.allclose(pointIterator.next(), (9, 0))
    assert np.allclose(pointIterator.next(), (1, 0))
    assert np.allclose(pointIterator.next(), (0, 1))
    assert np.allclose(pointIterator.next(), (0, 9))


def test_neighbours_right_boundary():

    point = (0, 5)
    pointIterator = automata.iterNeighbours(point, (10, 10), automata.CONNECT_4)

    assert np.allclose(pointIterator.next(), (9, 5))
    assert np.allclose(pointIterator.next(), (1, 5))
    assert np.allclose(pointIterator.next(), (0, 6))
    assert np.allclose(pointIterator.next(), (0, 4))


def test_neighbours_left_boundary():

    point = (5, 0)
    pointIterator = automata.iterNeighbours(point, (10, 10), automata.CONNECT_4)

    assert np.allclose(pointIterator.next(), (4, 0))
    assert np.allclose(pointIterator.next(), (6, 0))
    assert np.allclose(pointIterator.next(), (5, 1))
    assert np.allclose(pointIterator.next(), (5, 9))


def test_iterGrid():
    """ Assert the correct pattern of samples """

    grid = np.array([[1, 2], [3, 4]])
    gridIterator = automata.iterGrid(grid, automata.CONNECT_4)

    point, values = gridIterator.next()
    assert np.allclose(values, [3, 3, 2, 2])

    point, values = gridIterator.next()
    assert np.allclose(values, [4, 4, 1, 1])

    point, values = gridIterator.next()
    assert np.allclose(values, [1, 1, 4, 4])

    point, values = gridIterator.next()
    assert np.allclose(values, [2, 2, 3, 3])


def test_iterGrids():
    """ Assert the correct pattern of samples """

    grid1 = np.array([[1, 2], [3, 4]])
    grid2 = np.array([[5, 6], [7, 8]])
    gridsIterator = automata.iterGrids([grid1, grid2], automata.CONNECT_4)

    point, values = gridsIterator.next()
    assert np.allclose(values[0], [3, 3, 2, 2])
    assert np.allclose(values[1], [7, 7, 6, 6])

    point, values = gridsIterator.next()
    assert np.allclose(values[0], [4, 4, 1, 1])
    assert np.allclose(values[1], [8, 8, 5, 5])

    point, values = gridsIterator.next()
    assert np.allclose(values[0], [1, 1, 4, 4])
    assert np.allclose(values[1], [5, 5, 8, 8])

    point, values = gridsIterator.next()
    assert np.allclose(values[0], [2, 2, 3, 3])
    assert np.allclose(values[1], [6, 6, 7, 7])


def test_formSamples():
    """
    Assert that the correct pattern of samples is generated using both
    the fast and slow sampling methods.
    """

    grid, _ = np.mgrid[0:100, 0:100]

    gridIterator = automata.iterGrid(grid, automata.CONNECT_4)

    # Slow approach
    iteratorValues = []
    for _, values in gridIterator:
        iteratorValues.append(values)
    iteratorValues = np.array(iteratorValues)

    # Fast approach
    coordinates = automata.formSamples(grid.shape, automata.CONNECT_4)
    sampledValues = grid[coordinates]

    # Assert equivalence of approaches
    assert np.allclose(sampledValues, iteratorValues)


def test_flatten():
    """ Tests the flattening behavior of numpy"""
    # So : x.flatten() can be inverted using x.reshape(old_shape)
    grid = np.array([[1, 2, 4], [5, 6, 7]])
    assert np.allclose(grid.flatten().reshape(grid.shape), grid)
