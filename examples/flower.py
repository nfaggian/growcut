""" Example of grow-cut segmentation """

import numpy as np

from matplotlib import pyplot as plt

from growcut import growcut

# Load an image of a particular type
image = plt.imread('./examples/flower.png')
lum = np.average(image, 2)

# Form a label grid (0: no label, 1: foreground, 2: background)
label = np.zeros_like(lum, dtype=np.int)
label[75:90, 100:110] = 1
label[0:10, 0:10] = 2

# Form a strength grid.
strength = np.zeros_like(lum, dtype=np.float64)
strength[75:90, 100:110] = 1.0
strength[0:10, 0:10] = 1.0


# Plot the image and the label map.
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
ax1.imshow(lum, interpolation='nearest', cmap='gray')
ax1.axis('off')
ax2.imshow(label, interpolation='nearest', cmap='binary')
ax2.axis('off')

# Automate to update the labels
for i in range(200):
    strength, label = growcut.automate(lum, strength, label)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
ax1.imshow(lum, interpolation='nearest', cmap='gray')
ax1.axis('off')
ax2.imshow(label, interpolation='nearest', cmap='binary')
ax2.axis('off')

plt.show()
