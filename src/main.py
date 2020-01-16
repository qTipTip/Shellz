import bpy

bl_info = {
    "name": "Shellz",
    "blender": (2, 80, 0),
    "category": "object"
}


def register():
    print("Shellz is now running")
    bpy.utils.register_class(Shellz)


def unregister():
    print("Shellz is now disabled")
    bpy.utils.unregister_class(Shellz)


class Shellz(bpy.types.Operator):
    """
    Shellz tooltip
    """

    def execute(self, **kwargs):
        """
        This is run upon calling the operator
        """

        return {'FINISHED'}


if __name__ == '__main__':
    register()
