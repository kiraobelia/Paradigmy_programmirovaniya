from typing import Protocol


class GradingPolicy(Protocol):
    """Интерфейс политики расчета итогового балла."""
    def calculate(self, scores: list[float]) -> float:
        ...


class Student:
    """Класс студента с инкапсулированными данными."""
    def __init__(self, student_id: int, name: str) -> None:
        if isinstance(student_id, bool) or not isinstance(student_id, int) or student_id <= 0:
            raise ValueError("ID студента должен быть положительным целым числом")
        if not name or not name.strip():
            raise ValueError("Имя студента не может быть пустым")

        self.student_id = student_id
        self.name = name.strip()
        self._scores: list[float] = []

    def add_score(self, score: float) -> None:
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise TypeError("Балл должен быть числом")
        if not (0 <= score <= 100):
            raise ValueError("Балл должен быть в диапазоне от 0 до 100")
        self._scores.append(float(score))

    def get_scores(self) -> list[float]:
        return list(self._scores)  # Возвращаем копию для защиты состояния


class GradeBook:
    """Класс журнала успеваемости (Композиция с политикой оценивания)."""
    def __init__(self, policy: GradingPolicy) -> None:
        self._students: dict[int, Student] = {}
        self.policy = policy  # Передача зависимости через конструктор

    def add_student(self, student: Student) -> None:
        if student.student_id in self._students:
            raise ValueError(f"Студент с ID {student.student_id} уже существует")
        self._students[student.student_id] = student

    def get_student(self, student_id: int) -> Student:
        if student_id not in self._students:
            raise KeyError(f"Студент с ID {student_id} не найден")
        return self._students[student_id]

    def get_all_students(self) -> list[Student]:
        return list(self._students.values())
