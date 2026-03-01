#Attack.py - факторизация
import math

class Factorization:
    #n-разлогаемое число, iterat-ограничение итераций
    @staticmethod
    def Fermat(n, iterat=1000000):

        #Значение а
        a = math.isqrt(n)
        if a * a < n:
            a += 1

        iterations = 0

        #Перебор значений
        while iterations < iterat:
            b2 = a * a - n          #Вычисление квадрата b
            b = math.isqrt(b2)

            if b * b == b2:        #Проверка на полность квадрата
                return a - b, a + b     #Возврат множителей

            a += 1                      #Увеличение a если не найдены множетели
            iterations += 1


        return None         #Случай неудачи

