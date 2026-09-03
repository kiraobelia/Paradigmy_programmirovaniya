#Подсчитать кол-во простых чисел
numbers = [2, 4, 7, 9, 11, 15, 17, 20, 23]

count_primes = 0
prime_numbers = []

for number in numbers:
    if number > 1:
        is_prime = True
        for i in range(2, number):
            if number % i == 0:
                is_prime = False
                break
        if is_prime:
            prime_numbers.append(number)
            count_primes += 1

print("Простые числа:", prime_numbers)
print("Количество простых чисел:", count_primes)