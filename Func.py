#Func.py - основные функции программы

import random

#Проверка чисел, генерация простых чисел битовой длины
class Generator:
        #Статистический метод
        @staticmethod
        def MillerRabin(n, k=40):
            #n-проверяемое число, k-кол-во раундов проверки. Отель-триваго
            if n < 2:
                return False

            #Проверка на маленькие числа (для ускорения работы)
            smallpr = [2, 3, 5, 7, 11, 13, 17, 19, 23]

            if n in smallpr:
                return True         #Случай если число простое
            if any(n % p == 0 for p in smallpr):
                return False        #Случай если число составное

            #n-1 -> n-1 = 2^r*d, где d-нечетное число
            r = 0
            d = n - 1
            while d % 2 == 0:
                d //= 2
                r += 1

            #повторение k раз для повышения точности
            for _ in range(k):
                a = random.randrange(2, n - 2)      #Выбор случайного числа
                x = pow(a, d, n)                          #Модульная экспонента

                #Случай если x=1 или x=n-1 то тест является пройденым...
                if x == 1 or x == n - 1:
                    continue

                #...в ином случае вовзведение в квадрат продолжается
                for _ in range(r - 1):
                    x = pow(x, 2, n)
                    if x == n - 1:      #Тест пройден
                        break
                else:
                    return False        #Число не является составным

            return True     #Число простое

        @staticmethod
        def GeneratePrime(bit):
            #Генерация простого числа
            while True:
                number = random.getrandbits(bit)    #Генерация случайного числа длиной в биты
                number |= (1 << (bit - 1)) | 1      #Гарантия что число является  нечетным и битным

                #Проверка на простоту
                if Generator.MillerRabin(number):
                    return number

# Словарь
#def Diction():
#    name = {'bit': 'Размер ключа','c': 'Близкие простые','time': 'Время факторизации'}

#    return name
