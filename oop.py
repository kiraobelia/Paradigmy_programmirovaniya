#Подсчитать кол-во простых чисел
class PrimeAnalyzer:
    def __init__(self, numbers: list[int]):
        self._numbers = list(numbers)

    @staticmethod
    def _is_prime(number: int) -> bool:
        if number <= 1:
            return False
        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                return False
        return True

    def get_prime_numbers(self) -> list[int]:
        return [n for n in self._numbers if self._is_prime(n)]

    def count_primes(self) -> int:
        return len(self.get_prime_numbers())

analyzer = PrimeAnalyzer([2, 4, 7, 9, 11, 15, 17, 20, 23])
print("Простые числа:", analyzer.get_prime_numbers())
print("Количество простых чисел:", analyzer.count_primes())