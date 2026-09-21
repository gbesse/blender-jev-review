import unittest

from blender_jev_review.core import (
    detection_request,
    findings,
    issues_to_locate,
    location_request,
    selected_objects,
    validate_response,
)

PACK = {"id": "test", "issues": [{"id": "naming", "label": "Naming", "instructions": "Is a name ambiguous?", "mark_above": 0.6}]}


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.objects = selected_objects(
            [{"name": "Cube.001", "type": "MESH", "dimensions": [1, 2, 3], "polygons": 12, "materials": ["Material"]}]
        )

    def test_snapshot_is_bounded_and_exact(self):
        self.assertEqual(self.objects[0]["name"], "Cube.001")
        with self.assertRaisesRegex(ValueError, "select"):
            selected_objects([])
        self.assertEqual(len(selected_objects([{"name": str(i), "type": "EMPTY"} for i in range(300)])), 255)

    def test_two_pass_finds_exact_object(self):
        first_request = detection_request(self.objects, PACK)
        self.assertEqual(first_request["questions"]["naming"]["type"], "noul")
        first = {"model": "jev-1.13.0", "answers": {"naming": {"type": "noul", "noul": 0.9}}, "usage": {"input_tokens": 12}}
        validate_response(first, first_request["questions"])
        issues = issues_to_locate(first, PACK)
        second_request = location_request(self.objects, issues)
        second = {"model": "jev-1.13.0", "answers": {"naming": {"type": "choice", "choice": "object_1"}}, "usage": {"input_tokens": 10}}
        validate_response(second, second_request["questions"])
        self.assertEqual(findings(self.objects, issues, second)[0]["object_name"], "Cube.001")

    def test_rejects_invented_object(self):
        request = location_request(self.objects, PACK["issues"])
        response = {"model": "jev-1.13.0", "answers": {"naming": {"type": "choice", "choice": "invented"}}, "usage": {"input_tokens": 1}}
        with self.assertRaisesRegex(ValueError, "invalid choice"):
            validate_response(response, request["questions"])


if __name__ == "__main__":
    unittest.main()
