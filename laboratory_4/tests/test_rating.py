import unittest
from university_rating.calculations import calculate_average, determine_status
from university_rating.rating import build_rating, filter_passed
from university_rating.validation import validate_scores


class RatingTests(unittest.TestCase):
    def test_empty_average(self):
        self.assertIsNone(calculate_average([]))

    def test_status_boundary(self):
        self.assertEqual(determine_status(49.99), "не допущен")
        self.assertEqual(determine_status(50), "допущен")

    def test_invalid_score(self):
        with self.assertRaises(ValueError):
            validate_scores([80, 101])

    def test_source_is_not_changed(self):
        students = [{"id": 1, "name": "Test", "scores": [70, 80]}]
        before = [{"id": 1, "name": "Test", "scores": [70, 80]}]
        build_rating(students)
        self.assertEqual(students, before)

    # --- Новые тесты для Варианта 2 ---
    def test_filter_passed_returns_only_passed_students(self):
        students = [
            {"id": 101, "name": "Amina", "scores": [80, 90]},
            {"id": 102, "name": "Dias", "scores": [40, 45]},
        ]
        rating = build_rating(students)
        passed = filter_passed(rating)
        self.assertEqual(len(passed), 1)
        self.assertEqual(passed[0]["name"], "Amina")

    def test_filter_passed_empty_when_no_one_passed(self):
        students = [
            {"id": 102, "name": "Dias", "scores": [30, 40]},
        ]
        rating = build_rating(students)
        passed = filter_passed(rating)
        self.assertEqual(len(passed), 0)


if __name__ == "__main__":
    unittest.main()
