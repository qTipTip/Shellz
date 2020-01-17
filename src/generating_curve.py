import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from src.main import Ellipse

if __name__ == '__main__':
    C = Ellipse()

    theta = np.linspace(0, 10 * np.pi, 200)
    s = np.linspace(0, 2 * np.pi, 100)

    xyz = C(theta, s)

    fig = plt.figure()
    axs = Axes3D(fig)

    axs.plot_wireframe(*xyz)
    plt.show()
