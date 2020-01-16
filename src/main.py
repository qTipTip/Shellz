import bpy

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

        return {'FINISHED'}


if __name__ == '__main__':
    register()
