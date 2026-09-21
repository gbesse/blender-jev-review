"""Blender UI adapter for exact-object Jev review findings."""

import bpy
from bpy.props import StringProperty
from bpy.types import Operator, Panel

from .client import call_jev
from .core import detection_request, findings, issues_to_locate, location_request, selected_objects

PACK = {
    "id": "scene-hygiene",
    "issues": [
        {
            "id": "naming",
            "label": "Ambiguous naming",
            "instructions": "Does any selected object have a vague, default, or inconsistent production name?",
            "mark_above": 0.6,
        },
        {
            "id": "scale",
            "label": "Suspicious scale",
            "instructions": "Does any selected object's type, name, and dimensions suggest a likely scale or unit inconsistency?",
            "mark_above": 0.72,
        },
        {
            "id": "material",
            "label": "Material ambiguity",
            "instructions": "Does any selected mesh have material naming that is absent, default, or ambiguous for handoff?",
            "mark_above": 0.65,
        },
    ],
}

_results = []


def _snapshot(context):
    raw = []
    for obj in context.selected_objects:
        raw.append(
            {
                "name": obj.name,
                "type": obj.type,
                "dimensions": tuple(obj.dimensions),
                "polygons": len(obj.data.polygons) if obj.type == "MESH" else 0,
                "materials": [slot.material.name for slot in obj.material_slots if slot.material],
            }
        )
    return selected_objects(raw)


class JEV_OT_review(Operator):
    bl_idname = "jev.review_selection"
    bl_label = "Review selected objects"
    bl_options = {"REGISTER"}

    def execute(self, context):
        global _results
        try:
            objects = _snapshot(context)
            first_request = detection_request(objects, PACK)
            first = call_jev(first_request, context.window_manager.jev_api_key)
            issues = issues_to_locate(first, PACK)
            if not issues:
                _results = []
                self.report({"INFO"}, "No issue crossed the declared thresholds")
                return {"FINISHED"}
            second_request = location_request(objects, issues)
            second = call_jev(second_request, context.window_manager.jev_api_key)
            _results = findings(objects, issues, second)
            self.report({"INFO"}, f"{len(_results)} exact-object findings")
            return {"FINISHED"}
        except Exception as error:  # Blender operators surface errors through reports.
            self.report({"ERROR"}, str(error))
            return {"CANCELLED"}


class JEV_OT_focus(Operator):
    bl_idname = "jev.focus_object"
    bl_label = "Focus finding"
    object_name: StringProperty()

    def execute(self, context):
        obj = bpy.data.objects.get(self.object_name)
        if obj is None:
            self.report({"ERROR"}, "Cited object no longer exists")
            return {"CANCELLED"}
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        context.view_layer.objects.active = obj
        return {"FINISHED"}


class JEV_PT_panel(Panel):
    bl_label = "Jev Review"
    bl_idname = "JEV_PT_review"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Jev"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.window_manager, "jev_api_key", text="API key")
        layout.operator("jev.review_selection", icon="VIEWZOOM")
        for result in _results:
            row = layout.row()
            operator = row.operator("jev.focus_object", text=f"{result['issue']}: {result['object_name']}", icon="RESTRICT_SELECT_OFF")
            operator.object_name = result["object_name"]


CLASSES = (JEV_OT_review, JEV_OT_focus, JEV_PT_panel)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.jev_api_key = StringProperty(name="TypeSafe API key", subtype="PASSWORD", options={"SKIP_SAVE"})


def unregister():
    del bpy.types.WindowManager.jev_api_key
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
