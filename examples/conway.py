import numpy as np

from growcut import automata

from matplotlib import pyplot as plt
from matplotlib import animation


state = np.random.randint(0, 2, (100, 100)).astype(np.bool)
fig = plt.figure(figsize=(10, 10))
img = plt.imshow(state, interpolation='nearest', origin='lower', cmap='binary')


def init():
    img.set_data(state)
    return img,


def animate(i):
    state[:] = automata.gameOfLife(state)[:]
    img.set_data(state)
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
