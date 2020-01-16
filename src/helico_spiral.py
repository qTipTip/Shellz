import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class HelicoSpiral(object):

    def __init__(self, **kwargs):

        params = {'A': 1, 'beta': 0.5, 'alpha': 30}
        for parameter in params.keys():
            if parameter in kwargs.keys():
                params[parameter] = kwargs[parameter]

        self.params = params

    def __call__(self, theta):
        """
        Evaluates the helico-spiral at the scalar or array theta.
        Returns values (x, y, z).

        :param theta: point(s) to evaluate the spiral at
        :return: (x(theta), y(theta), z(theta))
        """

        theta = np.array(theta)

        A = self.params['A']
        beta = self.params['beta']
        alpha = self.params['alpha']

        cot = float(sp.cot(alpha))

        h = np.zeros((3, len(theta)))
        h[0] = np.sin(beta) * np.cos(theta) * np.exp(theta * cot)
        h[1] = np.sin(beta) * np.sin(theta) * np.exp(theta * cot)
        h[2] = -np.cos(beta) * np.exp(theta * cot)

        return A * h


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
