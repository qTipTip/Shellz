from mpl_toolkits.mplot3d import Axes3D

from src import Ellipse, HelicoSpiral

import numpy as np
import matplotlib.pyplot as plt

from src.main import Shell

if __name__ == '__main__':
    C = Ellipse(2, 1)
    H = HelicoSpiral(A=1, beta=100, alpha=30)

    S = Shell(H, C)

    theta = np.linspace(0, 2 * np.pi, 100)
    s = np.linspace(0, 2 * np.pi, 40)

    xyz = S(theta, s)

    fig = plt.figure()
    axs = Axes3D(fig)
    axs.plot_surface(*xyz, cmap=plt.cm.viridis)
    axs.plot(*H(theta))
    plt.show()
