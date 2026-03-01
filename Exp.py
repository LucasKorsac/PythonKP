# Exp.py - эксперимент

import time
import pandas as pd
from RSA import RSA
from Attack import Factorization


class Experiment:
    # samp - количество повторений, bit - размер RSA, c - близкие простые числа
    @staticmethod
    def run(samp=5, bit=64, c=False):

        result = []  # список результатов

        for _ in range(samp):
            # Генерация RSA
            rsa = RSA(bit=bit, close=c)

            # Время факторизации
            start = time.perf_counter()
            Factorization.Fermat(rsa.n)
            elapsed = time.perf_counter() - start

            # Сохранение результата
            result.append({'bit': bit, 'c': c, 'time': elapsed})

        # Создание таблицы
        df = pd.DataFrame(result)

        return df