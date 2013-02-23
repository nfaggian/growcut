import numpy as np

from growcut import automata

from matplotlib import pyplot as plt
from matplotlib import animation

state = np.random.randint(0, 2, (250, 250)).astype(np.bool)

coordinates = automata.formSamples(state.shape, neighbours=automata.CONNECT_8)

fig = plt.figure(figsize=(10, 10))
img = plt.imshow(state, interpolation='nearest', origin='lower', cmap='binary')
plt.axis('off')

def init():
    img.set_data(state)
    return img,


def animate(i):
    state[:] = automata.numpyGameOfLife(state, coordinates)[:]
    img.set_data(state)
    return img

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(
    fig,
    animate,
    init_func=init,
    frames=200,
    interval=1,
    blit=False
    )

plt.show()
