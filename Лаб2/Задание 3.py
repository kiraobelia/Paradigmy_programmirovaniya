score_input = input("Введите балл (от 0 до 100): ")

# Проверка ввода на число
try:
    score = float(score_input)
    
    # Проверка диапазона и определение оценки
    if score < 0 or score > 100:
        print("Ошибка: балл должен быть в диапазоне от 0 до 100.")
    elif score >= 90:
        print("Результат: A")
    elif score >= 75:
        print("Результат: B")
    elif score >= 50:
        print("Результат: C")
    else:
        print("Результат: F")
except ValueError:
    print("Ошибка: введено не числовое значение.")
