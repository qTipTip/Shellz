from numpy import sqrt, cosh, sinh, sin, cos, log, tan, pi, linspace, exp, deg2rad
import bpy


def cot(x):
    return 1 / tan(x)


class parametric_surface(object):
    """
    Contains methods for computing parametric equations, and generating a
    mesh for importing in Blender.
    """

    def __init__(self, u_range, v_range, u_resolution, v_resolution):

        self.u_start, self.u_end = u_range
        self.v_start, self.v_end = v_range

        self.u_resolution = u_resolution
        self.v_resolution = v_resolution

        self.name = '<Default>'

    def __call__(self, u, v):

        raise NotImplementedError

    def generate_mesh_data(self):
        """
        Given a surface object, returns a set of vertices and faces representing
        the surface.
        """
        vertices = []
        faces = []

        u_res = self.u_resolution
        v_res = self.v_resolution

        u_values = linspace(self.u_start, self.u_end, u_res)
        v_values = linspace(self.v_start, self.v_end, v_res)

        # compute vertices
        for u in u_values:
            for v in v_values:
                vertex = self(u, v)
                vertices.append(vertex)

        # compute faces
        counter = 0
        for i in range(0, v_res * (u_res - 1)):
            if counter < u_res - 1:
                # represents the corners of the face
                A = i
                B = i + 1
                C = (i + u_res) + 1
                D = (i + u_res)

                face = (A, B, C, D)
                faces.append(face)
                counter += 1

            else:
                counter = 0

        return vertices, faces


class dini_flower(parametric_surface):

    def __init__(self, u_resolution, v_resolution, a=1, b=0.2):
        parametric_surface.__init__(self, [0, 4 * pi], [0.0001, 2], u_resolution, v_resolution)
        self.a = a
        self.b = b

        self.name = 'Dini Flower'

    def __call__(self, u, v):
        a, b = self.a, self.b

        x = a * cos(u) * sin(v)
        y = a * sin(u) * sin(v)
        z = a * (cos(v) + log(tan(0.5 * v))) + b * u

        return x, y, z


class klein_bottle(parametric_surface):

    def __init__(self, u_resolution, v_resolution, a=3):
        parametric_surface.__init__(self, [0, 1.999 * pi], [0, 1.999 * pi], u_resolution, v_resolution)
        self.a = 3

        self.name = 'Klein Bottle'

    def __call__(self, u, v):
        a = self.a

        x = (a + cos(0.5 * u) * sin(v) - sin(0.5 * u) * sin(2 * v)) * cos(u)
        y = (a + cos(0.5 * u) * sin(v) - sin(0.5 * u) * sin(2 * v)) * sin(u)
        z = sin(0.5 * u) * sin(v) + cos(0.5 * u) * sin(2 * v)

        return x, y, z


class klein_bottle_classic(parametric_surface):

    def __init__(self, u_resolution, v_resolution, a=3):
        parametric_surface.__init__(self, [0, 0.999 * pi], [0, 1.999 * pi], \
                                    u_resolution, v_resolution)
        self.name = 'Klein Bottle (Classic)'

    def __call__(self, u, v):
        x = (-2 / 15.) * cos(u) * (3 * cos(v) - 30 * sin(u) + 90 * cos(u) ** 4 * sin(u) \
                                   - 60 * cos(u) ** 6 * sin(u) + 5 * cos(u) * cos(v) * sin(u))
        y = (-1 / 15.) * sin(u) * (3 * cos(v) - 3 * cos(u) ** 2 * cos(v) - \
                                   48 * cos(u) ** 2 * cos(v) + 48 * cos(u) ** 6 * cos(v) - \
                                   60 * sin(u) + 5 * cos(u) * cos(v) * sin(u) - 5 * cos(u) ** 3 * cos(v) * sin(u) - \
                                   80 * cos(u) ** 5 * cos(v) * sin(u) + 80 * cos(u) ** 7 * cos(v) * sin(u))
        z = (2 / 15.) * (3 + 5 * cos(u) * sin(u)) * sin(v)

        return x, y, z


class trefoil_knot(parametric_surface):

    def __init__(self, u_resolution, v_resolution, radius=1):
        parametric_surface.__init__(self, [-pi, 2 * pi], [-pi, 2 * pi], u_resolution, v_resolution)

        self.radius = 1
        self.name = 'Trefoil Knot'

    def __call__(self, u, v):
        radius = self.radius

        x = radius * sin(3 * u) / (2 + cos(v))
        y = radius * (sin(u) + 2 * sin(2 * u)) / (2 + cos(v + 2 * pi / 3))
        z = radius * 0.5 * (cos(u) - 2 * cos(2 * u)) * (2 + cos(v)) * (2 + cos(v + pi * 2 / 3)) / 4

        return x, y, z


# surface of choice

U_RESOLUTION = 40
V_RESOLUTION = 40

surface = klein_bottle(U_RESOLUTION, V_RESOLUTION)

mesh = bpy.data.meshes.new(surface.name)
blender_object = bpy.data.objects.new(surface.name, mesh)

blender_object.location = bpy.context.scene.cursor.location
bpy.context.collection.objects.link(blender_object)

vertices, faces = surface.generate_mesh_data()
print(vertices, faces)
mesh.from_pydata(vertices, [], faces)
mesh.update(calc_edges=True)
