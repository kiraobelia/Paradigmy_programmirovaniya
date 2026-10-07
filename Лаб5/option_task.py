class Student:
    """Модель студента для учебной группы."""

    def __init__(self, student_id, name, gpa=0.0):
        if student_id <= 0:
            raise ValueError("ID должен быть положительным числом")
        if not name.strip():
            raise ValueError("Имя не может быть пустым")
        self.student_id = student_id
        self.name = name.strip()
        self.gpa = float(gpa)


class AcademicGroup:
    """Учебная группа со старостой и составом."""

    def __init__(self, group_name):
        if not group_name.strip():
            raise ValueError("Название группы не должно быть пустым")
        self.group_name = group_name.strip()
        self._students = {}
        self._monitor = None

    def add_student(self, student):
        if not isinstance(student, Student):
            raise TypeError("Ожидается объект Student")
        if student.student_id in self._students:
            raise ValueError("Студент с таким ID уже есть в группе")
        self._students[student.student_id] = student

    def appoint_monitor(self, student_id):
        if student_id not in self._students:
            raise ValueError("Нельзя назначить старостой отсутствующего студента")
        self._monitor = self._students[student_id]

    @property
    def monitor(self):
        return self._monitor

    @property
    def group_average(self):
        if not self._students:
            return 0.0
        return sum(s.gpa for s in self._students.values()) / len(self._students)

    @property
    def students(self):
        return tuple(self._students.values())
