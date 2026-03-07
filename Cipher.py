# Cipher.py — Шифрование RSA
import random

#Проверка на простоту
def is_prime(num: int) -> bool:
    if num <= 1: return False    # Числа <= 1 не простые
    if num <= 3: return True     # Числа <= 1 не простые
    if num % 2 == 0 or num % 3 == 0: return False       # Кратные 2 или 3 — составные
    i = 5

    # Проверка делителей вида 6k ± 1 до sqrt(num)
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0: return False
        i += 6
    return True     # Делителей не найдено - число простое

#НОД
def gcd(a: int, b: int) -> int:
    while b != 0:              #Вычисление НОД двух чисел с помощью алгоритма Евклида
        a, b = b, a % b
    return a

# Расширенный алгоритм Евклида
def extended_gcd(a: int, b: int):
    if a == 0:                  #Возврат (gcd, x, y) такие, что a*x + b*y = gcd(a, b).
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

# Модульная инверсия
def mod_inverse(e: int, phi: int) -> int:
    gcd_val, x, _ = extended_gcd(e, phi)
    if gcd_val != 1:
        raise ValueError("Обратного элемента не существует")    # e и phi не взаимно простые
    return x % phi                   # Возврат положительного значения

# Класс RSA
class RSACrypto:

    # Инициализация ключевых параметров
    def __init__(self):
        self.n = 0
        self.e = 0
        self.d = 0
        self.p = 0
        self.q = 0

    # Генерация ключей
    def generate_keys(self, key_size: int = 12):
        # Генерация случайных простых чисел p и q
        self.p = self._generate_prime(key_size)
        self.q = self._generate_prime(key_size)
        while self.p == self.q:                          # Если случайно выпали одинаковые числа, генерация нового q
            self.q = self._generate_prime(key_size)

        self.n = self.p * self.q                     # Вычисление модуля n = p*q
        phi = (self.p - 1) * (self.q - 1)            # Функция Эйлера ф(n) = (p-1)*(q-1)

        self.e = 65537                               # Стандартная открытая экспонента

        # Если e не взаимно простое с phi, выбор случайного нечётного числа
        if gcd(self.e, phi) != 1:
            self.e = random.randrange(3, phi, 2)
            while gcd(self.e, phi) != 1:
                self.e = random.randrange(3, phi, 2)

        # Вычисление закрытой экспоненты d
        self.d = mod_inverse(self.e, phi)

        # Возврат параметров для проверки
        return self.p, self.q, self.n, self.e, self.d

    # Генерация случайного простого числа
    def _generate_prime(self, key_size: int):
        while True:
            num = random.getrandbits(key_size)      # случайное число key_size бит
            if num > 1 and is_prime(num):
                return num

    # Ручной ввод p и q
    def set_manual_keys(self, p: int, q: int):
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

    # Шифрование
    def encrypt(self, text: str) -> list:
        if self.n == 0:
            raise ValueError("Сначала сгенерируйте или установите ключи!")
        return [pow(ord(char), self.e, self.n) for char in text]    # Перевод каждого символа в число через ord, возведение в степень e по модулю n

    # Дешифрование
    def decrypt(self, ciphertext: list) -> str:
        if self.n == 0:
            raise ValueError("Ключи не сгенерированы!")
        return ''.join(chr(pow(c, self.d, self.n)) for c in ciphertext)     # Для малых n можно сразу использовать chr()
