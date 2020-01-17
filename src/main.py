import bpy
import numpy as np

bl_info = {
    "name": "Shellz",
    "blender": (2, 80, 0),
    "category": "object"
}


def register():
    bpy.utils.register_class(AddShell)


def unregister():
    bpy.utils.unregister_class(AddShell)


class AddShell(bpy.types.Operator):
    """
    Adds a shell based on the specified parameters.
    """
    bl_idname = 'object.add_shell'
    bl_label = "Adds a shell-object to the viewport"
    bl_options = {'Register', 'UNDO'}

    def execute(self, context):
        """
        This is run upon calling the operator
        """

        H = HelicoSpiral()
        C = Ellipse()
        S = Shell(H, C)

        theta = np.linspace(0, 2 * np.pi, 5)
        s = np.linspace(0, 2 * np.pi, 10)
        xyz = S(theta, s)
        faces = create_mesh(xyz)

        blender_import(context, xyz, faces)

        return {'FINISHED'}


def create_mesh(xyz):
    """
    Converts the data given in the xyz array of shape (3, m, n) to a format
    suitable for import into Blender.

    :param xyz:
    :return:
    """
    _, m, n = xyz.shape

    # compute faces
    counter = 0
    faces = []
    for i in range(0, n * (m - 1)):
        if counter < m - 1:
            # represents the corners of the face
            A = i
            B = i + 1
            C = (i + m) + 1
            D = (i + m)

            face = (A, B, C, D)
            faces.append(face)
            counter += 1
        else:
            counter = 0

    return faces


def blender_import(context: bpy.context, xyz, faces):
    mesh = bpy.data.meshes.new("Shell")
    blender_object = bpy.data.objects.new(mesh, "Shell")
    blender_object.location = context.scene.cursor_location


class GeneratingCurve(object):
    pass


def cot(alpha):
    return 1 / np.tan(alpha)


class Ellipse(GeneratingCurve):

    def __init__(self, a=1, b=1, alpha=30):
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
        cot = cot(self.alpha)

        x = cos_s * cos_theta * r * np.exp(theta * cot)
        y = cos_s * sin_theta * r * np.exp(theta * cot)
        z = sin_s * r * np.exp(theta * cot)

        return np.stack([x, y, z])

    def _radius(self, s):
        s = np.array(s)

        assert np.min(s) >= 0 and np.max(s) <= 2 * np.pi, "The parameter s must lie in the interval [0, 2*pi]"

        a, b = self.a, self.b
        return 1 / np.sqrt((np.cos(s) / a) ** 2 + (np.sin(s) / b) ** 2)


class Shell(object):

    def __init__(self, helico_spiral, generating_curve):
        """
        Initialize a shell by specifying the generating curve and the helico spiral.

        :param helico_spiral:
        :param generating_curve:
        """

        self.H = helico_spiral
        self.C = generating_curve

    def __call__(self, theta, s):
        return self.H(theta)[:, np.newaxis, :] + self.C(theta, s)


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

        cot = cot(alpha)

        h = np.zeros((3, len(theta)))
        h[0] = np.sin(beta) * np.cos(theta) * np.exp(theta * cot)
        h[1] = np.sin(beta) * np.sin(theta) * np.exp(theta * cot)
        h[2] = -np.cos(beta) * np.exp(theta * cot)

        return A * h


if __name__ == '__main__':
    register()
