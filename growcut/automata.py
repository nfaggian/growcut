""" Python implementation of growcut """

import numpy as np

CONNECT_4 = [(-1, 0), (1, 0), (0, 1), (0, -1)]
CONNECT_8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def iterNeighbours((r, c), shape, neighbours=CONNECT_4):
    """ Yield the point neighborhood """
    for (dr, dc) in neighbours:
        yield (r + dr) % shape[0], (c + dc) % shape[1]


def iterGrid(grid, neighbours=CONNECT_4):
    """ Iterate through a grid """
    for point in np.ndindex(grid.shape):
        values = [grid[x] for x in iterNeighbours(point, grid.shape, neighbours)]
        yield point, values


def gameOfLife(state):
    """ Conways game of life """

    nextState = np.zeros_like(state)

    for point, values in iterGrid(state, neighbours=CONNECT_8):

        liveNeigbhours = sum(values)

        alive = True if state[point] else False

        # Apply a set of rules.

        # Any live cell with fewer than two live neighbors dies, as if
        # caused by under-population.
        if alive and liveNeigbhours < 2:
            nextState[point] = 0

        # Any live cell with two or three live neighbors lives on to the
        # next generation.
        if alive and (liveNeigbhours == 2 or liveNeigbhours == 3):
            nextState[point] = 1

        # Any live cell with more than three live neighbors dies, as if by
        # overcrowding.
        if alive and liveNeigbhours > 3:
            nextState[point] = 0

        # Any dead cell with exactly three live neighbors becomes a live cell,
        # as if by reproduction.
        if not alive and liveNeigbhours == 3:
            nextState[point] = 1

    return nextState


# from scipy import ndimage
# from scipy import misc

# # Numpy approach.
# def vonNeumannSampler(shape):
#     sr = []
#     sc = []
#     for (r, c) in np.ndindex(shape):
#         sr.append([r-1, r+1, r, r])
#         sc.append([c, c, c+1, c-1])
#     return np.array(sr), np.array(sc)

