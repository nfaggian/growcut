""" Example of grow-cut segmentation """

import numpy as np

from growcut import automata, growcut

from matplotlib import pyplot as plt
from matplotlib import animation

import pyximport
pyximport.install(setup_args={"include_dirs": np.get_include()}, reload_support=True)
from growcut._automate_cy import automate_cy

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


#coordinates = automata.formSamples(lum.shape, neighbours=automata.CONNECT_4)

# Plot the image and the label map.
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
ax1.imshow(lum, interpolation='nearest', cmap='gray')
ax1.contour(label, colors='r')
ax1.axis('off')

img = ax2.imshow(label, interpolation='nearest', cmap='gray', vmin=0, vmax=1)
ax2.axis('off')


def init():
    img.set_data(label)
    return img,


def animate(i):
#    strength[:], label[:] = growcut.numpyAutomate(coordinates, lum, strength, label)
    strength[:], label[:] = automate_cy(lum, strength, label, connectivity=8)
    img.set_data((label == 1) * lum)
    return img,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(
    fig,
    animate,
    init_func=init,
    frames=200,
    interval=1,
    #blit=True
    )

plt.show()

