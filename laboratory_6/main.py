from typing import Protocol


# 1. Определение интерфейса (контракта) уведомителя
class Notifier(Protocol):
    """Интерфейс для отправки сообщений."""
    def send(self, recipient: str, message: str) -> None:
        ...


# 2. Реализации каналов уведомления
class ConsoleNotifier:
    """Уведомление через консоль."""
    def send(self, recipient: str, message: str) -> None:
        print(f"[Консоль -> {recipient}]: {message}")


class MemoryNotifier:
    """Сохранение сообщений в память (для тестов)."""
    def __init__(self) -> None:
        self.messages: list[tuple[str, str]] = []

    def send(self, recipient: str, message: str) -> None:
        self.messages.append((recipient, message))


class FileNotifier:
    """Уведомление с имитацией записи в файл/журнал."""
    def __init__(self, filename: str = "notifications.log") -> None:
        self.filename = filename

    def send(self, recipient: str, message: str) -> None:
        # Для демонстрации просто выводим факт "записи"
        print(f"[Запись в {self.filename}] {recipient}: {message}")


# 3. Модель студента
class Student:
    def __init__(self, student_id: int, name: str) -> None:
        if isinstance(student_id, bool) or not isinstance(student_id, int):
            raise TypeError("ID студента должен быть целым числом")
        if student_id <= 0:
            raise ValueError("ID должен быть положительным числом")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя студента не может быть пустым")

        self.student_id = student_id
        self.name = name.strip()
        self._scores: list[float] = []

    def add_score(self, score: float) -> None:
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise TypeError("Балл должен быть числовым значением")
        if not (0 <= score <= 100):
            raise ValueError("Балл должен находиться в диапазоне от 0 до 100")
        
        self._scores.append(float(score))

    @property
    def average_score(self) -> float | None:
        if not self._scores:
            return None
        return sum(self._scores) / len(self._scores)

    @property
    def status(self) -> str:
        avg = self.average_score
        if avg is None:
            return "нет данных"
        return "допущен" if avg >= 50.0 else "не допущен"


# 4. Класс журнала оценок (Композиция)
class GradeBook:
    def __init__(self, notifier: Notifier) -> None:
        self._students: dict[int, Student] = {}
        self._notifier = notifier  # Передача зависимости через конструктор

    def register_student(self, student: Student) -> None:
        if student.student_id in self._students:
            raise ValueError(f"Студент с ID {student.student_id} уже зарегистрирован")
        self._students[student.student_id] = student

    def add_score_to_student(self, student_id: int, score: float) -> None:
        student = self._find_student(student_id)
        student.add_score(score)

    def notify_student(self, student_id: int) -> None:
        student = self._find_student(student_id)
        text = f"Ваш текущий статус: {student.status}"
        # Делегирование отправки объекту-уведомителю
        self._notifier.send(student.name, text)

    def _find_student(self, student_id: int) -> Student:
        if student_id not in self._students:
            raise KeyError(f"Студент с ID {student_id} не найден")
        return self._students[student_id]


# Демонстрация работы
if __name__ == "__main__":
    print("--- Запуск с ConsoleNotifier ---")
    console_notif = ConsoleNotifier()
    gb1 = GradeBook(console_notif)
    
    st1 = Student(101, "Хуснора")
    gb1.register_student(st1)
    gb1.add_score_to_student(101, 75)
    gb1.add_score_to_student(101, 82)
    gb1.notify_student(101)

    print("\n--- Запуск с FileNotifier (проверка взаимозаменяемости) ---")
    file_notif = FileNotifier("log.txt")
    gb2 = GradeBook(file_notif)
    
    st2 = Student(102, "Алижан")
    gb2.register_student(st2)
    gb2.add_score_to_student(102, 40)
    gb2.notify_student(102)
