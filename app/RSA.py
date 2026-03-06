# app/RSA.py
import random
import math
from app.Func import Generator


class RSA:
    """Класс для работы с RSA шифрованием"""

    def __init__(self, bit=1024, c=False, st=False):
        """
        bit - размер ключа в битах
        c - использовать близкие простые числа (уязвимость)
        st - использовать сильные простые числа
        """
        # Генерация p и q
        if st:
            self.p = Generator.GenStrongPr(bit // 2)
            self.q = Generator.GenStrongPr(bit // 2)
        else:
            self.p = Generator.GenPr(bit // 2)
            self.q = Generator.GenPr(bit // 2)

        # Приближение q к p (режим уязвимости)
        if c:
            delt = random.randint(2, 100)
            self.q = self.p + delt
            while not Generator.MillerRabin(self.q):
                self.q += 1

        # Валидация
        assert Generator.MillerRabin(self.p), f"p не простое!"
        assert Generator.MillerRabin(self.q), f"q не простое!"
        assert self.p != self.q, "p и q совпадают!"

        # Вычисление параметров RSA
        self.n = self.p * self.q
        phi = (self.p - 1) * (self.q - 1)
        self.e = 65537

        while math.gcd(self.e, phi) != 1:
            self.e += 2

        self.d = pow(self.e, -1, phi)

    def encrypt(self, message: str) -> list:
        """Шифрует строку, возвращая список чисел"""
        cipher_text = [pow(ord(char), self.e, self.n) for char in message]
        return cipher_text

    def decrypt(self, cipher_list: list) -> str:
        """Расшифровывает список чисел в строку"""
        plain_codes = [pow(c, self.d, self.n) for c in cipher_list]

        result = []
        for i, code in enumerate(plain_codes):
            if not (0 <= code <= 0x10FFFF):
                raise ValueError(f"Некорректный декодированный код: {code} на позиции {i}")
            result.append(chr(code))

        return "".join(result)

    def test_keys(self, test_message="ABC"):
        """Проверка корректности ключей"""
        try:
            encrypted = self.encrypt(test_message)
            decrypted = self.decrypt(encrypted)
            return decrypted == test_message
        except:
            return False