"""Blender Jev Review add-on package and host-safe registration shim."""

bl_info = {
    "name": "Jev Selected Object Review",
    "author": "Guillaume Besse",
    "version": (0, 1, 0),
    "blender": (4, 3, 0),
    "location": "View3D > Sidebar > Jev",
    "description": "Review selected object metadata and focus exact cited objects",
    "category": "3D View",
}


def register():
    from .addon import register as register_addon

    register_addon()


def unregister():
    from .addon import unregister as unregister_addon

    unregister_addon()
