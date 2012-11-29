""" Tests for the growcut module """

import numpy as np

from growcut import growcut, automata


def test_g():
    """ Assert the pattern the dampening function is correct """

    maxC = 100
    assert np.allclose(growcut.g(100, maxC), 0.0, atol=0.1)
    assert np.allclose(growcut.g(50, maxC), 0.5, atol=0.1)
    assert np.allclose(growcut.g(0, maxC), 1.0, atol=0.1)


def test_norm():
    # Uses the well tested numpy norm - no need to test.
    pass


def test_automate():

    shape = (20, 20)
    cx, cy = shape[1] / 2.0, shape[0] / 2.0
    r = 5

    y, x = np.ogrid[0:shape[0], 0:shape[1]]
    mask = (np.power((y - cy), 2) + np.power((x - cx), 2)) < np.power(r, 2)

    field = np.zeros(mask.shape)
    field[mask] = 1.0
    label = np.zeros_like(field)
    theta = np.zeros_like(field)
    label[:] = 0

    label[0:(r / 4), 0:(r / 4)] = -1
    theta[0:(r / 4), 0:(r / 4)] = 1.0

    label[cy - (r / 4):cy + (r / 4), cx - (r / 4):cx + (r / 4)] = 1
    theta[cy - (r / 4):cy + (r / 4), cx - (r / 4):cx + (r / 4)] = 1.0

    # Plot the image and the label map.
    # import matplotlib.pyplot as plt
    # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    # ax1.imshow(field, interpolation='nearest', cmap='gray')
    # ax1.axis('off')
    # ax2.imshow(label, interpolation='nearest', cmap='jet')
    # ax2.axis('off')

    # Automate to update the labels
    for itteration in range(100):
        theta, label = growcut.automate(field, theta, label)

    # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    # ax1.imshow(field, interpolation='nearest', cmap='gray')
    # ax1.axis('off')
    # ax2.imshow(label, interpolation='nearest', cmap='jet')
    # ax2.axis('off')
    # plt.show()

    # Assert that the label map looks like the mask
    assert np.allclose(label[mask], 1.0) & np.allclose(label[~mask], -1), \
        "Segmentation did not converge after {} iterations".format(itteration)


def test_numpy_automate():

    shape = (100, 100)
    cx, cy = shape[1] / 2.0, shape[0] / 2.0
    r = 20

    y, x = np.ogrid[0:shape[0], 0:shape[1]]
    mask = (np.power((y - cy), 2) + np.power((x - cx), 2)) < np.power(r, 2)

    field = np.zeros(mask.shape)
    field[mask] = 1.0
    label = np.zeros_like(field)
    theta = np.zeros_like(field)
    label[:] = 0

    label[0:(r / 4), 0:(r / 4)] = -1
    theta[0:(r / 4), 0:(r / 4)] = 1.0

    label[cy - (r / 4):cy + (r / 4), cx - (r / 4):cx + (r / 4)] = 1
    theta[cy - (r / 4):cy + (r / 4), cx - (r / 4):cx + (r / 4)] = 1.0

    # Plot the image and the label map.
    # import matplotlib.pyplot as plt
    # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    # ax1.imshow(field, interpolation='nearest', cmap='gray')
    # ax1.axis('off')
    # ax2.imshow(label, interpolation='nearest', cmap='jet')
    # ax2.axis('off')

    coordinates = automata.formSamples(field.shape, neighbours=automata.CONNECT_8)

    # Automate to update the labels
    for itteration in range(100):
        theta, label = growcut.numpyAutomate(coordinates, field, theta, label)

    # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    # ax1.imshow(field, interpolation='nearest', cmap='gray')
    # ax1.axis('off')
    # ax2.imshow(label, interpolation='nearest', cmap='jet')
    # ax2.axis('off')
    # plt.show()

    # Assert that the label map looks like the mask
    assert np.allclose(label[mask], 1.0) & np.allclose(label[~mask], -1), \
        "Segmentation did not converge after {} iterations".format(itteration)
