import unittest
from option_task import AcademicGroup, Student as GroupStudent
from student import Student


class Lab5Tests(unittest.TestCase):
    #Тест базовых классов
    def test_student_average_and_snapshot(self):
        student = Student(1, "Amina", "IS-24-1")
        student.add_score(80)
        student.add_score(90)
        self.assertEqual(student.scores, (80.0, 90.0))
        self.assertEqual(student.average, 85.0)

    #5 тестов Варианта 6
    def test_add_student_success(self):
        group = AcademicGroup("TII-25-21")
        s = GroupStudent(1, "Karina", 90.0)
        group.add_student(s)
        self.assertEqual(len(group.students), 1)

    def test_appoint_monitor_success(self):
        group = AcademicGroup("TII-25-21")
        s = GroupStudent(1, "Karina", 90.0)
        group.add_student(s)
        group.appoint_monitor(1)
        self.assertEqual(group.monitor.name, "Karina")

    def test_group_average(self):
        group = AcademicGroup("TII-25-21")
        group.add_student(GroupStudent(1, "Student 1", 80.0))
        group.add_student(GroupStudent(2, "Student 2", 100.0))
        self.assertEqual(group.group_average, 90.0)

    def test_appoint_missing_student_as_monitor_raises_error(self):
        group = AcademicGroup("TII-25-21")
        with self.assertRaises(ValueError):
            group.appoint_monitor(999)  # Ошибочный сценарий 1

    def test_add_duplicate_student_raises_error(self):
        group = AcademicGroup("TII-25-21")
        s1 = GroupStudent(1, "Karina", 90.0)
        s2 = GroupStudent(1, "Other", 80.0)
        group.add_student(s1)
        with self.assertRaises(ValueError):
            group.add_student(s2)  # Ошибочный сценарий 2


if __name__ == "__main__":
    unittest.main()
