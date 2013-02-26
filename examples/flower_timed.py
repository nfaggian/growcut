""" Example of grow-cut segmentation, should be run from package root """

import numpy as np

from growcut import automata, growcut

import pyximport
pyximport.install(setup_args={"include_dirs": np.get_include()},
                  reload_support=True)
from growcut._automate_cy import automate_cy

from matplotlib import pyplot as plt
import time

# Load an image of a particular type
image = plt.imread('./examples/flower.png')
lum = np.average(image, 2).astype(np.float64)

# Form a label grid (0: no label, 1: foreground, 2: background)
label = np.zeros_like(lum, dtype=np.int)
label[:] = -1
label[75:90, 100:110] = 1
label[110:120, 150:160] = 1
label[50:55, 160:165] = 1
label[50:55, 180:185] = 0
label[0:10, 0:10] = 0
label[75:90, 0:10] = 0
label[0:10, 200:210] = 0
label[75:90, 200:210] = 0

# Form a strength grid.
strength = np.zeros_like(lum, dtype=np.float64)
strength[label != -1] = 1.0


t0 = time.time()
coordinates = automata.formSamples(lum.shape, neighbours=automata.CONNECT_4)
strength, label = growcut.numpyAutomate(coordinates, lum, strength, label)
print "Numpy vectorized: " + str(1000 * (time.time() - t0)) + " ms"

t0 = time.time()
strength, label = automate_cy(lum, strength, label, connectivity=4)
print "Cython: " + str(1000 * (time.time() - t0)) + " ms"

t0 = time.time()
strength, label = growcut.automate(lum, strength, label)
print "Pure Python: " + str(1000 * (time.time() - t0)) + " ms"
