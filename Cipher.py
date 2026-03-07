# rsa_crypto.py — ОТДЕЛЬНЫЙ ФАЙЛ ДЛЯ ПУНКТА 4.2.6
import random

def is_prime(num: int) -> bool:
    """Проверка на простоту (достаточно для лабораторной)"""
    if num <= 1: return False
    if num <= 3: return True
    if num % 2 == 0 or num % 3 == 0: return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0: return False
        i += 6
    return True

def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a: int, b: int):
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def mod_inverse(e: int, phi: int) -> int:
    gcd_val, x, _ = extended_gcd(e, phi)
    if gcd_val != 1:
        raise ValueError("Обратного элемента не существует")
    return x % phi


class RSACrypto:
    def __init__(self):
        self.n = 0
        self.e = 0
        self.d = 0
        self.p = 0
        self.q = 0

    def generate_keys(self, key_size: int = 12):
        """Автогенерация ключей (подходит для лабораторной)"""
        self.p = self._generate_prime(key_size)
        self.q = self._generate_prime(key_size)
        while self.p == self.q:
            self.q = self._generate_prime(key_size)

        self.n = self.p * self.q
        phi = (self.p - 1) * (self.q - 1)

        self.e = 65537
        if gcd(self.e, phi) != 1:
            self.e = random.randrange(3, phi, 2)
            while gcd(self.e, phi) != 1:
                self.e = random.randrange(3, phi, 2)

        self.d = mod_inverse(self.e, phi)
        return self.p, self.q, self.n, self.e, self.d

    def _generate_prime(self, key_size: int):
        while True:
            num = random.getrandbits(key_size)
            if num > 1 and is_prime(num):
                return num

    def set_manual_keys(self, p: int, q: int):
        """Ручной ввод p и q"""
        if not is_prime(p) or not is_prime(q):
            raise ValueError("p и q должны быть простыми числами")
        if p == q:
            raise ValueError("p и q должны быть разными")
        self.p, self.q = p, q
        self.n = p * q
        phi = (p - 1) * (q - 1)
        self.e = 65537
        if gcd(self.e, phi) != 1:
            self.e = 3
        self.d = mod_inverse(self.e, phi)

    def encrypt(self, text: str) -> list:
        """Шифрование (посимвольно)"""
        if self.n == 0:
            raise ValueError("Сначала сгенерируйте или установите ключи!")
        return [pow(ord(char), self.e, self.n) for char in text]

    def decrypt(self, ciphertext: list) -> str:
        """Дешифрование"""
        if self.n == 0:
            raise ValueError("Ключи не сгенерированы")
        return ''.join(chr(pow(c, self.d, self.n)) for c in ciphertext)
