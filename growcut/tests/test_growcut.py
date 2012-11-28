""" Tests for the growcut module """

import numpy as np

from growcut import growcut


def test_g():
    """ Assert the pattern the dampening function is correct """

    C = [10., 20., 30.]

    assert np.allclose(growcut.g(10, C), 0.6, atol=0.1)
    assert np.allclose(growcut.g(20, C), 0.3, atol=0.1)
    assert np.allclose(growcut.g(30, C), 0.0, atol=0.1)

    C = [128., 128., 128.]

    assert np.allclose(growcut.g(10, C), 0.9, atol=0.1)
    assert np.allclose(growcut.g(20, C), 0.8, atol=0.1)
    assert np.allclose(growcut.g(30, C), 0.7, atol=0.1)
    assert np.allclose(growcut.g(40, C), 0.6, atol=0.1)


def test_norm():
    # Uses the well tested numpy norm - no need to test.
    pass
