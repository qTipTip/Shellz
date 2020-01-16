from mpl_toolkits.mplot3d import Axes3D

from src.generating_curve import Ellipse
from src.helico_spiral import HelicoSpiral

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt


class Shell(object):

    def __init__(self, helico_spiral, generating_curve):
        """

        :param helico_spiral:
        :param generating_curve:
        """

        self.H = helico_spiral
        self.C = generating_curve

    def __call__(self, theta, s):
        return self.H(theta)[:, np.newaxis, :] + self.C(theta, s)


if __name__ == '__main__':
    C = Ellipse(2, 1)
    H = HelicoSpiral()

    S = Shell(H, C)

    theta = np.linspace(0, 4 * np.pi, 100)
    s = np.linspace(0, 2 * np.pi, 20)

    xyz = S(theta, s)

    fig = plt.figure()
    axs = Axes3D(fig)
    axs.plot_surface(*xyz)
    axs.plot(*H(theta))
    plt.show()
