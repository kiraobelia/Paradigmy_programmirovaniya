import unittest
from main import Student, GradeBook, MemoryNotifier, ConsoleNotifier


class TestGradeBookSystem(unittest.TestCase):

    def setUp(self) -> None:
        self.mem_notifier = MemoryNotifier()
        self.grade_book = GradeBook(self.mem_notifier)

    def test_successful_registration_and_notification(self) -> None:
        student = Student(1, "Карина")
        self.grade_book.register_student(student)
        self.grade_book.add_score_to_student(1, 90)
        self.grade_book.add_score_to_student(1, 85)
        
        self.grade_book.notify_student(1)
        
        # Проверяем, что сообщение сохранилось в MemoryNotifier
        self.assertEqual(len(self.mem_notifier.messages), 1)
        self.assertEqual(
            self.mem_notifier.messages[0],
            ("Карина", "Ваш текущий статус: допущен")
        )

    def test_student_not_found_error(self) -> None:
        with self.assertRaises(KeyError):
            self.grade_book.notify_student(999)

    def test_invalid_score_raises_exception(self) -> None:
        student = Student(2, "{Хуснора")
        with self.assertRaises(ValueError):
            student.add_score(150)  # Оценка больше 100

    def test_duplicate_registration_raises_error(self) -> None:
        st1 = Student(3, "Бекзат")
        st2 = Student(3, "Дамир")
        self.grade_book.register_student(st1)
        
        with self.assertRaises(ValueError):
            self.grade_book.register_student(st2)

    def test_interchangeability_of_notifiers(self) -> None:
        # Проверка, что GradeBook одинаково работает с любым Notifier
        console_notif = ConsoleNotifier()
        gb = GradeBook(console_notif)
        st = Student(4, "Сабина")
        gb.register_student(st)
        gb.add_score_to_student(4, 60)
        
        # Метод не должен вызывать ошибок
        try:
            gb.notify_student(4)
        except Exception as e:
            self.fail(f"notify_student вызвал исключение: {e}")


if __name__ == "__main__":
    unittest.main()
