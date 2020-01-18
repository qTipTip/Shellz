import bpy
import bmesh
import numpy as np

from mathutils import Vector

bl_info = {
    "name": "Shellz",
    "blender": (2, 80, 0),
    "category": "object"
}


def cotan(x):
    return 1 / np.tan(x)


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
    bl_options = {'REGISTER', 'UNDO'}

    # Properties: General
    resolution: bpy.props.IntProperty(
        name="resolution",
        default=40
    )
    alpha: bpy.props.FloatProperty(
        name="alpha",
        default=30,
        min=0,
        max=180,
    )

    # Properties: Helico Spiral
    thetaMin: bpy.props.FloatProperty(
        name="min(theta)",
        default=0.0,
    )
    thetaMax: bpy.props.FloatProperty(
        name="max(theta)",
        default=360
    )
    beta: bpy.props.FloatProperty(
        name="beta",
        default=30,
        min=0,
        max=180
    )
    A: bpy.props.FloatProperty(
        name="A",
        default=1
    )

    # Properties: Generating Curve

    sMin: bpy.props.FloatProperty(
        name="min(s)",
        default=0
    )
    sMax: bpy.props.FloatProperty(
        name="max(s)",
        default=360
    )
    omega: bpy.props.FloatProperty(
        name="omega",
        default=0
    )
    phi: bpy.props.FloatProperty(
        name="phi",
        default=0
    )
    mu: bpy.props.FloatProperty(
        name="mu",
        default=0
    )

    a: bpy.props.FloatProperty(
        name="a",
        default=1,
    )
    b: bpy.props.FloatProperty(
        name="b",
        default=1
    )

    # Properties: Nodules
    N: bpy.props.IntProperty(
        name="N",
        default=0,
        min=0
    )
    P: bpy.props.FloatProperty(
        name="P",
        default=0,
        min=0,
        max=360
    )
    W_1: bpy.props.FloatProperty(
        name="W_1",
        default=0
    )
    W_2: bpy.props.FloatProperty(
        name="W_2",
        default=0
    )
    L: bpy.props.FloatProperty(
        name="L",
        default=0
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        """
        This is run upon calling the operator
        """

        H = HelicoSpiral(alpha=np.deg2rad(self.alpha), beta=np.deg2rad(self.beta), A=self.A)
        C = Ellipse(a=self.a, b=self.b, A=self.A, alpha=np.deg2rad(self.alpha), beta=np.deg2rad(self.beta),
                    omega=np.deg2rad(self.omega), phi=np.deg2rad(self.phi),
                    mu=np.deg2rad(self.mu), L=self.L, P=np.deg2rad(self.P), N=self.N, W_1=self.W_1, W_2=self.W_2)
        S = Shell(H, C)

        theta = np.linspace(np.deg2rad(self.thetaMin), np.deg2rad(self.thetaMax), self.resolution)
        s = np.linspace(np.deg2rad(self.sMin), np.deg2rad(self.sMax), self.resolution)
        xyz = S(theta, s)
        vertices, faces = create_mesh(xyz)

        blender_import(context, vertices, faces)

        return {'FINISHED'}


def create_mesh(xyz):
    """
    Converts the data given in the xyz array of shape (3, m, n) to a format
    suitable for import into Blender.

    :param xyz:
    :return:
    """
    _, m, n = xyz.shape

    # compute vertices
    vertices = []
    for i in range(m):
        for j in range(n):
            vertices.append(tuple(xyz[:, i, j]))
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

    return vertices, faces


def blender_import(context: bpy.context, vertices, faces):
    mesh = bpy.data.meshes.new("Shell")
    blender_object = bpy.data.objects.new("Shell", mesh)
    blender_object.location = bpy.context.scene.cursor.location

    bpy.context.collection.objects.link(blender_object)
    mesh.from_pydata(vertices, [], faces)
    # mesh.update(calc_edges=True)

    normalize_object_size(blender_object)


def normalize_object_size(blender_object):
    # Eventually apply transforms (comment if unwanted)
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    minX = min([vertex.co[0] for vertex in blender_object.data.vertices])
    minY = min([vertex.co[1] for vertex in blender_object.data.vertices])
    minZ = min([vertex.co[2] for vertex in blender_object.data.vertices])
    vMin = Vector([minX, minY, minZ])
    maxDim = max(blender_object.dimensions)
    if maxDim != 0:
        for v in blender_object.data.vertices:
            v.co -= vMin  # Set all coordinates start from (0, 0, 0)
            v.co /= maxDim  # Set all coordinates between 0 and 1
    else:
        for v in blender_object.data.vertices:
            v.co -= vMin


class GeneratingCurve(object):
    pass


def cot(alpha):
    return 1 / np.tan(alpha)


class Ellipse(GeneratingCurve):

    def __init__(self, a=1, b=1, A=1, alpha=30, beta=30, omega=0, phi=0, mu=0, L=0, N=0, W_1=0, W_2=0, P=0):
        """
        Initializes an elliptical generating curve with semi-axes a and b.

        :param a: semi-axis
        :param b: semi-axis
        """

        self.a = a
        self.b = b
        self.A = A
        self.alpha = alpha
        self.beta = beta
        self.omega = omega
        self.phi = phi
        self.mu = mu
        self.L = L
        self.N = N
        self.W_1 = W_1
        self.W_2 = W_2
        self.P = P

    def __call__(self, theta, s):
        """
        Evaluates the ellipse at the point (theta, s). The ellipse is assumed to grow
        at the same rate as the helico spiral in these specific equations.

        :param theta:
        :param s:
        :return:
        """

        theta, s = np.meshgrid(theta, s)

        r = self._radius(s) + self._nodules(s, theta)
        theta = np.array(theta)

        cos_s = np.cos(s + self.phi)
        sin_s = np.sin(s + self.phi)

        cos_theta = np.cos(theta + self.omega)
        sin_theta = np.sin(theta + self.omega)
        cot = cotan(self.alpha)

        x = cos_s * cos_theta * r * np.exp(theta * cot)
        y = cos_s * sin_theta * r * np.exp(theta * cot)
        z = sin_s * r * np.exp(theta * cot)

        # Adding rotation in the mu-plane
        x = x - (z.copy() * np.sin(self.mu)) * sin_theta
        y = y + (z.copy() * np.sin(self.mu)) * cos_theta
        z = (-self.A * np.cos(self.beta) + np.cos(self.mu) * sin_s * r) * np.exp(theta * cot)

        return np.stack([x, y, z])

    def _radius(self, s):
        s = np.array(s)

        # assert np.min(s) >= 0 and np.max(s) <= 2 * np.pi, "The parameter s must lie in the interval [0, 2*pi]"

        a, b = self.a, self.b
        return 1 / np.sqrt((np.cos(s) / a) ** 2 + (np.sin(s) / b) ** 2)

    def _nodules(self, s, theta):
        if self.W_1 == 0 or self.W_2 == 0 or self.N == 0:
            return np.zeros_like(s)
        else:
            l_theta = 2 * np.pi / self.N * (self.N * theta / (2 * np.pi) - np.round(self.N * theta / 2 * np.pi))
            return self.L * np.exp(-((2 * (s - self.P) / self.W_1) ** 2 + (2 * l_theta / self.W_2) ** 2))


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

        cot = cotan(alpha)

        h = np.zeros((3, len(theta)))
        h[0] = np.sin(beta) * np.cos(theta) * np.exp(theta * cot)
        h[1] = np.sin(beta) * np.sin(theta) * np.exp(theta * cot)
        h[2] = -np.cos(beta) * np.exp(theta * cot)

        return A * h


if __name__ == '__main__':
    register()
