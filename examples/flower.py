""" Example of grow-cut segmentation """

import numpy as np

from growcut import automata, growcut

from matplotlib import pyplot as plt
from matplotlib import animation


# Load an image of a particular type
image = plt.imread('./examples/flower.png')
lum = np.average(image, 2)

# Form a label grid (0: no label, 1: foreground, 2: background)
label = np.zeros_like(lum, dtype=np.int)
label[:] = -1
label[75:90, 100:110] = 1
label[0:10, 0:10] = 0
label[75:90, 0:10] = 0
label[0:10, 200:210] = 0
label[75:90, 200:210] = 0

# Form a strength grid.
strength = np.zeros_like(lum, dtype=np.float64)
strength[75:90, 100:110] = 1.0
strength[0:10, 0:10] = 1.0
strength[75:90, 0:10] = 1.0
strength[0:10, 200:210] = 1.0
strength[75:90, 200:210] = 1.0


coordinates = automata.formSamples(lum.shape, neighbours=automata.CONNECT_8)

# Plot the image and the label map.
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
ax1.imshow(lum, interpolation='nearest', cmap='gray')
ax1.axis('off')
img = ax2.imshow(label, interpolation='nearest', cmap='binary')
ax2.axis('off')


def init():
    img.set_data(label)
    return img,


def animate(i):
    strength[:], label[:] = growcut.numpyAutomate(coordinates, lum, strength, label)
    img.set_data(label)
    return img,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(
    fig,
    animate,
    init_func=init,
    frames=200,
    interval=1,
    blit=True
    )

plt.show()

