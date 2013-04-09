""" Tests for the growcut module """

import pytest
import numpy as np

from growcut import growcut, growcut_cy


def sample_data(shape):
    """ Forms a circle to segment """

    shape = (20, 20)
    cx, cy = shape[1] / 2.0, shape[0] / 2.0
    r = 5

    y, x = np.ogrid[0:shape[0], 0:shape[1]]
    mask = (np.power((y - cy), 2) + np.power((x - cx), 2)) < np.power(r, 2)

    image = np.zeros(mask.shape)
    image[mask] = 1.0

    label = np.zeros_like(image)
    strength = np.zeros_like(image)

    label[0:(r / 4), 0:(r / 4)] = -1
    strength[0:(r / 4), 0:(r / 4)] = 1.0

    label[cy - (r / 4):cy + (r / 4), cx - (r / 4):cx + (r / 4)] = 1
    strength[cy - (r / 4):cy + (r / 4), cx - (r / 4):cx + (r / 4)] = 1.0

    return image, mask, label, strength


@pytest.mark.parametrize(("shape"), [(10, 10), (20, 20), (40, 40)])
def test_growcut(shape):
    """ Test correct segmentations using growcut """

    image, mask, label, strength = sample_data(shape)

    segmentation = growcut.growcut(
        image,
        np.dstack((label, strength)),
        window_size=3)

    assert np.allclose(mask, segmentation == 1), "Segmentation did not converge"


#@pytest.mark.parametrize(("shape"), [(10, 10), (20, 20), (40, 40)])
#def test_growcut_cython_equality(shape):
#    """ Test correct segmentations using growcut """
#
#    image, mask, label, strength = sample_data(shape)
#
#    segmentation_slow = growcut.growcut(
#        image,
#        np.dstack((label, strength)),
#        window_size=3)
#
#    segmentation_fast = growcut_cy.growcut(
#        np.array([image, image, image]),
#        np.dstack((label, strength)),
#        window_size=3)
#
#    assert np.allclose(segmentation_slow, segmentation_fast), \
#        "Optimized segmentation is not equivalent to slow version."
