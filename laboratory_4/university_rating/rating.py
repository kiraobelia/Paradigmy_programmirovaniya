from .calculations import calculate_average, determine_status
from .validation import validate_scores, validate_student


def build_student_result(student):
    """Формирует новую итоговую запись одного студента."""
    validate_student(student)
    scores = validate_scores(student["scores"])
    average = calculate_average(scores)
    return {
        "id": student["id"],
        "name": student["name"],
        "average": average,
        "status": determine_status(average),
    }


def _sort_key(item):
    average = item["average"]
    return average is not None, average or 0


def build_rating(students):
    """Возвращает рейтинг, не изменяя исходные записи."""
    results = [build_student_result(item) for item in students]
    return sorted(results, key=_sort_key, reverse=True)

# --- Индивидуальное задание (Вариант 2) ---
def filter_passed(rating):
    """Возвращает только тех студентов, у которых статус 'допущен'."""
    return [student for student in rating if student["status"] == "допущен"]
