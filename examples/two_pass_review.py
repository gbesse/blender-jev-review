"""Synthetic two-pass object review using the Blender-independent core."""
import json

from blender_jev_review.core import (
    detection_request,
    findings,
    issues_to_locate,
    location_request,
    selected_objects,
    validate_response,
)

PACK = {
    "id": "synthetic-scene-hygiene",
    "issues": [{"id": "name", "label": "Ambiguous name", "instructions": "Is the object name ambiguous?", "mark_above": 0.6}],
}
objects = selected_objects(
    [
        {"name": "Cube.001", "type": "MESH", "dimensions": [1, 1, 1]},
        {"name": "Cube.001", "type": "MESH", "dimensions": [1, 2, 1]},
    ]
)
first = detection_request(objects, PACK)
first_answer = {"model": "jev-1.13.0", "answers": {"name": {"type": "noul", "noul": 0.9}}, "usage": {"input_tokens": 12}}
validate_response(first_answer, first["questions"])
issues = issues_to_locate(first_answer, PACK)
second = location_request(objects, issues)
second_answer = {"model": "jev-1.13.0", "answers": {"name": {"type": "choice", "choice": "object_2"}}, "usage": {"input_tokens": 10}}
validate_response(second_answer, second["questions"])
assert objects[0]["name"] == objects[1]["name"] and objects[0]["id"] != objects[1]["id"]
try:
    validate_response(
        {"model": "jev-1.13.0", "answers": {"name": {"type": "choice", "choice": "invented"}}, "usage": {"input_tokens": 10}},
        second["questions"],
    )
except ValueError:
    invented_rejected = True
else:
    invented_rejected = False
assert invented_rejected
print(
    json.dumps(
        {
            "source": "synthetic fixture; no Blender or network",
            "findings": findings(objects, issues, second_answer),
            "invented_object_rejected": invented_rejected,
        },
        sort_keys=True,
    )
)
