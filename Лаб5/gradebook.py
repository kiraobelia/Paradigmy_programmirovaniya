from student import Student

class GradeBook:
    """Журнал регистрации и оценки студентов."""

    def __init__(self):
        self._students = {}

    def register(self, student):
        if not isinstance(student, Student):
            raise TypeError("Ожидается объект Student")
        if student.student_id in self._students:
            raise ValueError("Студент уже зарегистрирован")
        self._students[student.student_id] = student

    def add_score(self, student_id, score):
        try:
            student = self._students[student_id]
        except KeyError as error:
            raise KeyError("Студент не найден") from error
        student.add_score(score)

    def find(self, student_id):
        return self._students.get(student_id)

    def rating(self):
        return tuple(
            sorted(
                self._students.values(),
                key=lambda student: (
                    student.average is not None,
                    student.average or 0,
                ),
                reverse=True,
            )
        )
