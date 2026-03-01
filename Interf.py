#Interf.py - интерфейс

import tkinter as tk
from tkinter import ttk, messagebox
import threading

import Func
from Exp import Experiment
import Graph

#Интерфейс
class Gui:
    #Инициализация
    def __init__(self, root):
        self.root = root
        self.root.title("RSA")

        self.result = None

        ttk.Label(root, text="Размер ключа:").grid(row=0, column=0) #Поле ввода ключа
        self.bitsentry = ttk.Entry(root)
        self.bitsentry.insert(0, "64")      #Значение по умолчанию
        self.bitsentry.grid(row=0, column=1)

        ttk.Label(root, text="Количество экспериментов:").grid(row=1, column=0) #Поле ввода кол-ва экспериментов
        self.sampentry = ttk.Entry(root)
        self.sampentry.insert(0, "3")       #Значение по умолчанию
        self.sampentry.grid(row=1, column=1)

        self.clvar = tk.BooleanVar()        #Быстрый взлом

        ttk.Checkbutton(root, text="Быстрый взлом", variable=self.clvar).grid(row=2, column=0, columnspan=2) #Отметка

        ttk.Button(root, text="Запустить", command=self.RunExper).grid(row=3, column=0, columnspan=2, pady=10)    #Запуск программы

        ttk.Button(root, text="Построить график", command=self.GraphEr).grid(row=4, column=0, columnspan=2)  #Построение графика

        self.output = tk.Text(root, height=10, width=50)
        self.output.grid(row=5, column=0, columnspan=2, pady=10)

    #Запуск эксперимента
    def RunExper(self):
        thread = threading.Thread(target=self.RunThread)
        thread.start()

    def RunThread(self):
        try:
            #Чтение полей
            bit = int(self.bitsentry.get())
            samp = int(self.sampentry.get())
            c = self.clvar.get()

            #Очистка поля вывода
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, "Выполняется...\n")

            #Запуск эксперимента
            df = Experiment.run(samp=samp, bit=bit, c=c)

            self.result = df    #Сохранение результата

            ttime = df["time"].mean()       #Расчет времени

            self.output.insert(tk.END, f"\nСреднее время: {ttime:.6f} сек\n")
            self.output.insert(tk.END, str(df))

        #Обработка ошибок
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    # Построение графика
    def GraphEr(self):
        if self.result is None:
            messagebox.showwarning("Внимание", "Сначала выполните эксперимент")
            return

        #График средних значений
        Graph.PlotRes(self.result)

        # График всех экспериментов
        Graph.PlotExperiments(self.result)

#Запуск
if __name__ == "__main__":
    root = tk.Tk()
    app = Gui(root)
    root.mainloop()