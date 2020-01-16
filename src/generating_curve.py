import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class GeneratingCurve(object):
    pass


class Ellipse(GeneratingCurve):

    def __init__(self, a=1, b=1, alpha=0.1):
        """
        Initializes an elliptical generating curve with semi-axes a and b.

        :param a: semi-axis
        :param b: semi-axis
        """

        self.a = a
        self.b = b
        self.alpha = alpha

    def __call__(self, theta, s):
        """
        Evaluates the ellipse at the point (theta, s). The ellipse is assumed to grow
        at the same rate as the helico spiral in these specific equations.

        :param theta:
        :param s:
        :return:
        """

        theta, s = np.meshgrid(theta, s)

        r = self._radius(s)
        theta = np.array(theta)

        n = r.shape[0]
        m = theta.shape[0]

        cos_s = np.cos(s)
        sin_s = np.sin(s)

        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        cot = float(sp.cot(self.alpha))

        x = cos_s * cos_theta * r * np.exp(theta * cot)
        y = cos_s * sin_theta * r * np.exp(theta * cot)
        z = sin_s * r * np.exp(theta * cot)

        return np.stack([x, y, z])

    def _radius(self, s):
        s = np.array(s)

        assert np.min(s) >= 0 and np.max(s) <= 2 * np.pi, "The parameter s must lie in the interval [0, 2*pi]"

        a, b = self.a, self.b
        return np.sqrt((np.cos(s) / a) ** 2 + (np.sin(s) / b) ** 2)


if __name__ == '__main__':
    C = Ellipse()

    theta = np.linspace(0, 10 * np.pi, 20)
    s = np.linspace(0, 2 * np.pi, 10)

    xyz = C(theta, s)

    fig = plt.figure()
    axs = Axes3D(fig)

    axs.plot_wireframe(*xyz)
    plt.show()
