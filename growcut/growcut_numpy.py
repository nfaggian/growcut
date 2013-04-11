""" Implementation of the grow-cut algorithm """

from __future__ import division

import numpy as np

from skimage import img_as_float
from math import sqrt

import logging


def g(x, y):
    return 1 - np.sqrt(np.sum((x - y) ** 2)) / sqrt(3)


def G(x, y):
    return 1 - np.sqrt((x - y) ** 2) / sqrt(3)


def growcut(image, state, max_iter=100, window_size=5):
    """Grow-cut segmentation.

    Parameters
    ----------
    image : (M, N) ndarray
        Input image.
    state : (2, M, N) ndarray
        Initial state, which stores (foreground/background, strength) for
        each pixel position or automaton.  The strength represents the
        certainty of the state (e.g., 1 is a hard seed value that remains
        constant throughout segmentation).
    max_iter : int, optional
        The maximum number of automata iterations to allow.  The segmentation
        may complete earlier if the state no longer varies.
    window_size : int
        Size of the neighborhood window.

    Returns
    -------
    mask : ndarray
        Segmented image.  A value of zero indicates background, one foreground.

    """
    image = img_as_float(image)
    height, width = image.shape[:2]
    ws = (window_size - 1) // 2

    state_next = state.copy()

    changing = 1

    for n in range(0, max_iter):

        if not changing:
            break

        changing = 0

        for coord in np.ndindex(height, width):
            i, j = coord

            C_p = image[i, j]
            S_p = state[:, i, j]

            window = (
                slice(max(0, i - ws), min(i + ws + 1, height)),
                slice(max(0, j - ws), min(j + ws + 1, width))
                )

            C_q = image[window]
            S_q_label = state[0][window]
            S_q_strength = state[1][window]

            gc = G(C_q, C_p)

            # Compute the strength mask
            mask = (gc * S_q_strength) > S_p[1]

            if np.any(mask):
                state_next[0, i, j] = (S_q_label[mask])[0]
                state_next[1, i, j] = (gc * S_q_strength)[mask][0]
                changing += 1

        state = state_next

    return state[0]

