# Модуль шифрования RSA


class RSACipher:
    def __init__(self, n, e, d):
        # Инициализация шифратора RSA. n : int - модуль RSA (p*q), e : int - открытая экспонента, d : int - закрытая экспонента
        self.n = n
        self.e = e
        self.d = d

    # Шифрование текста
    def encrypt(self, text):
        cipher = []

        for ch in text:
            m = ord(ch)  # Преобразование символа в число (код Unicode)
            c = pow(m, self.e, self.n)  # Шифрование: c = m^e mod n
            cipher.append(c)  # Список зашифрованных чисел

        return cipher

    # Дешифрование
    def decrypt(self, data):

        text = ""

        for c in data:
            m = pow(c, self.d, self.n)  # Дешифрование: m = c^d mod n
            text += chr(m)  # Преобразование числа в символ

        return text
