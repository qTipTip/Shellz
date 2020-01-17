import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from src.main import HelicoSpiral

if __name__ == '__main__':
    H = HelicoSpiral()

    t = np.linspace(0, 10 * np.pi, 100)
    h = H(t)

    fig = plt.figure()
    axs = Axes3D(fig)
    axs.set_zlim3d(-1, 0.1)
    axs.set_xlim3d(-1, 1)
    axs.set_ylim3d(-1, 1)

    axs.plot(*h)
    plt.show()
