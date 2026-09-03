#Подсчитать кол-во простых чисел
def is_prime(n: int) -> bool:
    return n > 1 and all(n % i != 0 for i in range(2, int(n ** 0.5) + 1))

numbers = [2, 4, 7, 9, 11, 15, 17, 20, 23]

# Вариант с filter и len
result_filter = len(list(filter(is_prime, numbers)))

# Вариант через генераторное выражение и sum ( True считается как 1 )
result_sum = sum(1 for n in numbers if is_prime(n))

print("Результат (filter):", result_filter)
print("Результат (генератор):", result_sum)