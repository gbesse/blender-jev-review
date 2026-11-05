import unittest

from blender_jev_review.core import selection_diff


class SelectionDiffTests(unittest.TestCase):
    def test_dimensions_change_without_rename(self):
        a = [{"id": "object_1", "name": "Cube", "dimensions": [1, 1, 1]}]
        b = [{"id": "object_1", "name": "Cube", "dimensions": [1, 2, 1]}]
        self.assertEqual(selection_diff(a, b)["changed"], ["object_1"])

    def test_order_only_unchanged(self):
        a = [{"id": "a", "name": "A"}, {"id": "b", "name": "B"}]
        self.assertTrue(selection_diff(a, list(reversed(a)))["unchanged"])

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            selection_diff([{"id": "a"}, {"id": "a"}], [])
