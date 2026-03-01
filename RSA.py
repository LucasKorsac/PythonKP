#RSA.py - генерация ключей

import random
from Func import Generator

#Создание параметров RSA
class RSA:

    #Инициализация класса
    def __init__(self, bit=64, close=False):

        #Простые числа
        self.p = Generator.GeneratePrime(bit // 2)
        self.q = Generator.GeneratePrime(bit // 2)

        # Приблежение q к p  в целях демонстрации  уязвимости RSA
        if close:
            delta = random.randint(2, 100)      #Смещение
            self.q = self.p + delta                   #Увеличение q
            while not Generator.MillerRabin(self.q):    #Проверка q на простоту
                self.q += 1

        #Вычисление модуля RSA
        self.n = self.p * self.q