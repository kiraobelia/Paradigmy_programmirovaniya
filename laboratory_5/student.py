class Student:
    """Студент с защищённой коллекцией оценок."""

    def __init__(self, student_id, name, group):
        if isinstance(student_id, bool) or not isinstance(student_id, int):
            raise TypeError("Идентификатор должен быть целым числом")
        if student_id <= 0:
            raise ValueError("Идентификатор должен быть положительным")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя не должно быть пустым")
        if not isinstance(group, str) or not group.strip():
            raise ValueError("Группа не должна быть пустой")

        self.student_id = student_id
        self.name = name.strip()
        self.group = group.strip()
        self._scores = []

    def add_score(self, score):
        """Добавляет корректный балл."""
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise TypeError("Балл должен быть числом")
        if not 0 <= score <= 100:
            raise ValueError("Балл должен быть от 0 до 100")
        self._scores.append(float(score))

    @property
    def scores(self):
        """Возвращает неизменяемый снимок оценок."""
        return tuple(self._scores)

    @property
    def average(self):
        """Возвращает среднее значение или None при отсутствии оценок."""
        if not self._scores:
            return None
        return sum(self._scores) / len(self._scores)

    @property
    def status(self):
        """Возвращает статус допуска по среднему баллу."""
        if self.average is None:
            return "нет данных"
        return "допущен" if self.average >= 50 else "не допущен"

    def __repr__(self):
        return (
            f"Student(student_id={self.student_id!r}, "
            f"name={self.name!r}, group={self.group!r})"
        )
