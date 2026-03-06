# app/Func.py
import random


class Generator:
    """Генерация и проверка простых чисел"""

    @staticmethod
    def MillerRabin(n, k=40):
        """
        Вероятностный тест Миллера-Рабина на простоту
        n - проверяемое число
        k - количество раундов проверки
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False

        # Представление n-1 = 2^r * d
        r, d = 0, n - 1
        while d % 2 == 0:
            d //= 2
            r += 1

        # k раундов проверки
        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)

            if x == 1 or x == n - 1:
                continue

            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False  # Число составное

        return True  # Все раунды пройдены - число простое

    @staticmethod
    def GenPr(bit):
        """Генерация обычного простого числа заданной битовой длины"""
        while True:
            number = random.getrandbits(bit)
            number |= (1 << (bit - 1)) | 1  # Старший и младший бит = 1
            if Generator.MillerRabin(number):
                return number

    @staticmethod
    def GenStrongPr(bit):
        """Генерация сильного простого числа (p = 2*q1*q2 + 1)"""
        while True:
            q1 = Generator.GenPr(bit // 2)
            q2 = Generator.GenPr(bit // 2)
            p = 2 * q1 * q2 + 1
            if Generator.MillerRabin(p):
                return p