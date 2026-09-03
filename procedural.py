#Подсчитать кол-во простых чисел
def is_prime(number: int) -> bool:
    if number <= 1:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True

def count_prime_numbers(values: list[int]) -> int:
    count = 0
    for number in values:
        if is_prime(number):
            count += 1
    return count

numbers = [2, 4, 7, 9, 11, 15, 17, 20, 23]
result = count_prime_numbers(numbers)
print("Количество простых чисел:", result)