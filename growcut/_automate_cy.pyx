#cython: cdivision=True
#cython: boundscheck=False
#cython: nonecheck=False
#cython: wraparound=False

import sys
import numpy as np
cimport numpy as cnp

cdef tuple CONNECT_4 = ((-1, 0), (1, 0), (0, 1), (0, -1))
cdef tuple CONNECT_8 = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
                        (0, 1), (1, -1), (1, 0), (1, 1))

if sys.version_info < (3,):
    range = xrange


def _pad(arr):
    arr = np.vstack((arr[0, :], arr, arr[arr.shape[0] - 1, :]))
    return np.hstack((arr[:, 0][:, np.newaxis],
                      arr,
                      arr[:, arr.shape[1] - 1][:, np.newaxis]))


def automate_cy(cnp.ndarray[cnp.float64_t, ndim=2] lum,
                cnp.ndarray[cnp.float64_t, ndim=2] strength,
                cnp.ndarray[cnp.int_t, ndim=2] label,
                connectivity=4):
    """ Grow-cut with Cython """
    if connectivity == 4:
        connectivity = CONNECT_4
    else:
        connectivity = CONNECT_8

    # Output initialization
    cdef cnp.ndarray[cnp.float64_t, ndim=2] nextStrength = (
                np.atleast_2d(strength.copy()))
    cdef cnp.ndarray[cnp.int_t, ndim=2] nextLabel = (
                np.atleast_2d(label.copy()))

    # Internal variables
    cdef:
        tuple rel_point
        float cp, thetap, cq, thetaq, lum_max, test
        int lq
        Py_ssize_t rows = lum.shape[0]
        Py_ssize_t cols = lum.shape[1]
        Py_ssize_t rel_row, rel_col, offset_row, offset_col

    # Set max luminance
    lum_max = lum.max()

    # Pad inputs with one pixel of replication, so wraparound isn't a concern
    lum = _pad(lum)
    strength = _pad(strength)
    label = _pad(label)

    # Loop over every point
    for row in range(rows):
        for col in range(cols):
            offset_row = row + 1
            offset_col = col + 1
            cp = lum[offset_row, offset_col]
            thetap = strength[offset_row, offset_col]

            # Loop over local neighborhood
            for rel_point in connectivity:
                rel_row = row + rel_point[0] + 1
                rel_col = col + rel_point[1] + 1
                cq = lum[rel_row, rel_col]
                thetaq = strength[rel_row, rel_col]
                lq = label[rel_row, rel_col]
                test = (1 - (abs(cp - cq) / lum_max)) * thetaq

                if test > thetap:
                    nextLabel[row, col] = lq
                    nextStrength[row, col] = test

    return nextStrength, nextLabel
