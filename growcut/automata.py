""" Python implementation of grow-cut """

import numpy as np

from scipy import ndimage as nd


CONNECT_4 = [(-1, 0), (1, 0), (0, 1), (0, -1)]
CONNECT_8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


# Slow neighborhood generator functions.

def iterNeighbours((r, c), shape, neighbours=CONNECT_4):
    """ Yield the point neighborhood """
    for (dr, dc) in neighbours:
        yield (r + dr) % shape[0], (c + dc) % shape[1]


def iterGrid(grid, neighbours=CONNECT_4):
    """ Iterate through a grid """
    for point in np.ndindex(grid.shape):
        values = [grid[x] for x in iterNeighbours(point, grid.shape, neighbours)]
        yield point, values


# Fast equivalent numpy/scipy functions.

def formSamples(shape, neighbours=CONNECT_4):
    """ Forms a matrix of row and sample coordinates """
    sr = []
    sc = []
    r, c = np.mgrid[0:shape[0], 0:shape[1]]
    for (dr, dc) in neighbours:
        sr.append((r.flatten() + dr) % shape[0])
        sc.append((c.flatten() + dc) % shape[1])

    coordinates = np.array(sr).T, np.array(sc).T
    return coordinates


def sample(grid, coordinates):
    """ Samples a grid at the specified coordinates """
    return nd.map_coordinates(grid, coordinates, order=0)


def numpyGameOfLife(state, coordinates):
    """ Conways game of life """

    neighboursStates = sample(state, coordinates)

    alive = state.flatten()

    nextState = np.zeros_like(alive)

    aliveNeighbours = neighboursStates.sum(axis=1)

    # Any live cell with fewer than two live neighbors dies, as if
    # caused by under-population.
    nextState[alive & (aliveNeighbours < 2)] = False

    # Any live cell with two or three live neighbors lives on to the
    # next generation.
    nextState[alive & np.logical_or(aliveNeighbours == 2, aliveNeighbours == 3)] = True

    # Any live cell with more than three live neighbors dies, as if by
    # overcrowding.
    nextState[alive & (aliveNeighbours > 3)] = False

    # Any dead cell with exactly three live neighbors becomes a live cell,
    # as if by reproduction.
    nextState[(~alive) & (aliveNeighbours == 3)] = True

    return nextState.reshape(state.shape)


# Game of life using python generators.

def gameOfLife(state):
    """ Conways game of life """

    nextState = np.zeros_like(state)

    for point, values in iterGrid(state, neighbours=CONNECT_8):

        aliveNeigbhours = sum(values)

        alive = True if state[point] else False

        # Apply a set of rules.

        # Any live cell with fewer than two live neighbors dies, as if
        # caused by under-population.
        if alive and aliveNeigbhours < 2:
            nextState[point] = 0

        # Any live cell with two or three live neighbors lives on to the
        # next generation.
        if alive and (aliveNeigbhours == 2 or aliveNeigbhours == 3):
            nextState[point] = 1

        # Any live cell with more than three live neighbors dies, as if by
        # overcrowding.
        if alive and aliveNeigbhours > 3:
            nextState[point] = 0

        # Any dead cell with exactly three live neighbors becomes a live cell,
        # as if by reproduction.
        if not alive and aliveNeigbhours == 3:
            nextState[point] = 1

    return nextState
