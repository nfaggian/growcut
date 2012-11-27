""" Python implementation of growcut """

import numpy as np

NEIGHBOURS = [(-1, 0), (1, 0), (0, 1), (0, -1)]


def iterNeighbours((r, c), shape, neighbours=NEIGHBOURS):
    """ Yield the point neighborhood """
    for (dr, dc) in neighbours:
        yield (r + dr) % shape[0], (c + dc) % shape[1]


def iterGrid(grid):
    """ Iterate through a grid """
    for point in np.ndindex(grid.shape):
        values = [grid[x] for x in iterNeighbours(point, grid.shape)]
        yield point, values


def gameOfLife(state):
    """ Conways game of life """

    nextState = np.zeros_like(state)

    for point, values in iterGrid(state):

        liveNeigbhours = sum(values)

        # Any live cell with fewer than two live neighbors dies, as if
        # caused by under-population.
        if liveNeigbhours < 2:
            nextState[point] = 0

        # Any live cell with two or three live neighbors lives on to the
        # next generation.
        if liveNeigbhours == 2 or liveNeigbhours == 3:
            nextState[point] = 1

        # Any live cell with more than three live neighbors dies, as if by
        # overcrowding.
        if liveNeigbhours > 3:
            nextState[point] = 0

        # Any dead cell with exactly three live neighbors becomes a live cell,
        # as if by reproduction.
        if not state[point] and liveNeigbhours > 3:
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

