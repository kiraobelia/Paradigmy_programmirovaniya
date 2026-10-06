PASSING_AVERAGE = 50


def calculate_average(scores):
    """Возвращает среднее или None для пустой последовательности."""
    return sum(scores) / len(scores) if scores else None


def determine_status(average):
    """Возвращает статус по среднему баллу."""
    if average is None:
        return "нет данных"
    return "допущен" if average >= PASSING_AVERAGE else "не допущен"
