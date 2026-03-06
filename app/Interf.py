# app/Interface.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading

from app.Func import Generator
from app.Exp import Experiment
from app import Graph
from app.RSA import RSA


class Gui:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA - Криптоанализ и Шифрование")
        self.root.geometry("650x700")
        
        self.rsa = None      # Ключи RSA для шифрования
        self.res = None      # Результаты эксперимента

        # ═══════════════════════════════════════════════════
        # 1️⃣ ПАРАМЕТРЫ ЭКСПЕРИМЕНТА
        # ═══════════════════════════════════════════════════
        ttk.Label(root, text="📊 Параметры эксперимента", font=("Arial", 10, "bold")).pack(pady=10)
        
        ttk.Label(root, text="Размер ключа (бит):").pack(pady=2)
        self.bitsentry = ttk.Entry(root, width=20)
        self.bitsentry.insert(0, "64")
        self.bitsentry.pack()

        ttk.Label(root, text="Количество экспериментов:").pack(pady=2)
        self.sampentry = ttk.Entry(root, width=20)
        self.sampentry.insert(0, "5")
        self.sampentry.pack()

        # Тип простых чисел
        self.prtype = tk.StringVar(value="normal")
        ttk.Label(root, text="Тип простых чисел:").pack(pady=5)

        radfr = ttk.Frame(root)
        radfr.pack(pady=5)
        ttk.Radiobutton(radfr, text="Обычные", variable=self.prtype, value="normal").pack(side="left", padx=10)
        ttk.Radiobutton(radfr, text="Близкие", variable=self.prtype, value="close").pack(side="left", padx=10)
        ttk.Radiobutton(radfr, text="Сильные", variable=self.prtype, value="strong").pack(side="left", padx=10)

        # Кнопка эксперимента
        ttk.Button(root, text="🚀 Запустить эксперимент", command=self.RunExper).pack(pady=10)

        # ═══════════════════════════════════════════════════
        # 2️⃣ КНОПКИ УПРАВЛЕНИЯ
        # ═══════════════════════════════════════════════════
        btnfr = ttk.Frame(root)
        btnfr.pack(pady=10)
        
        ttk.Button(btnfr, text="🔑 Генерация ключей", command=self.GenWindow).pack(side="left", padx=5)
        ttk.Button(btnfr, text="📈 Графики", command=self.GraphWindow).pack(side="left", padx=5)
        ttk.Button(btnfr, text="🔐 Шифрование", command=self.CipherWindow).pack(side="left", padx=5)

        # ═══════════════════════════════════════════════════
        # 3️⃣ ПОЛЕ ВЫВОДА
        # ═══════════════════════════════════════════════════
        ttk.Label(root, text="📝 Результаты:", font=("Arial", 10, "bold")).pack(pady=(15, 5))
        self.output = tk.Text(root, height=12, width=70)
        self.output.pack(pady=5, fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.output, command=self.output.yview)
        scrollbar.pack(side="right", fill="y")
        self.output.config(yscrollcommand=scrollbar.set)

        # Статус бар
        self.status = ttk.Label(root, text="Готов", relief="sunken", anchor="w")
        self.status.pack(fill="x", pady=5)

    # ═══════════════════════════════════════════════════
    # ЭКСПЕРИМЕНТ
    # ═══════════════════════════════════════════════════
    def RunExper(self):
        thread = threading.Thread(target=self.ExperThread, daemon=True)
        thread.start()

    def ExperThread(self):
        try:
            bit = int(self.bitsentry.get())
            samp = int(self.sampentry.get())

            if bit < 32 or bit > 512:
                messagebox.showwarning("Предупреждение", "Размер ключа: 32-512 бит")
                return
            if samp < 1 or samp > 100:
                messagebox.showwarning("Предупреждение", "Экспериментов: 1-100")
                return

            ptype = self.prtype.get()
            close = ptype == "close"
            strong = ptype == "strong"

            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, f"⚙️ Параметры:\n")
            self.output.insert(tk.END, f"   Размер: {bit} бит | Экспериментов: {samp} | Тип: {ptype}\n\n")
            self.output.insert(tk.END, "⏳ Выполняется...\n")
            self.status.config(text="Эксперимент выполняется...")
            self.root.update()

            df = Experiment.run(samp=samp, bit=bit, c=close, st=strong)
            self.res = df

            avg = df["time"].mean()
            self.output.insert(tk.END, f"\n✅ Среднее время: {avg:.6f} сек\n\n")
            self.output.insert(tk.END, str(df))
            self.status.config(text="Готов")

        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте числовые значения")
            self.status.config(text="Ошибка ввода")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
            self.status.config(text="Ошибка")

    # ═══════════════════════════════════════════════════
    # ГЕНЕРАЦИЯ КЛЮЧЕЙ
    # ═══════════════════════════════════════════════════
    def GenWindow(self):
        genwin = tk.Toplevel(self.root)
        genwin.title("Генерация ключей RSA")
        genwin.geometry("500x400")
        genwin.grab_set()

        ttk.Label(genwin, text="Размер ключа (бит):").pack(pady=5)
        bitent = ttk.Entry(genwin, width=20)
        bitent.insert(0, "512")
        bitent.pack()

        typeprine = tk.StringVar(value="normal")
        ttk.Radiobutton(genwin, text="Обычные (Миллер-Рабин)", variable=typeprine, value="normal").pack(pady=5)
        ttk.Radiobutton(genwin, text="Сильные простые", variable=typeprine, value="strong").pack(pady=5)
        ttk.Radiobutton(genwin, text="Близкие (уязвимые)", variable=typeprine, value="close").pack(pady=5)

        output = tk.Text(genwin, height=10, width=55)
        output.pack(pady=10, fill="both", expand=True)

        def Generate():
            try:
                bit = int(bitent.get())
                if bit < 64 or bit > 2048:
                    messagebox.showwarning("Предупреждение", "Размер: 64-2048 бит")
                    return

                close = typeprine.get() == "close"
                strong = typeprine.get() == "strong"

                rsa = RSA(bit=bit, c=close, st=strong)
                self.rsa = rsa
                self.params = {"n": rsa.n, "e": rsa.e, "d": rsa.d}

                output.delete("1.0", tk.END)
                output.insert(tk.END, f"✅ Ключи сгенерированы!\n\n")
                output.insert(tk.END, f"p = {rsa.p}\n")
                output.insert(tk.END, f"q = {rsa.q}\n")
                output.insert(tk.END, f"n = {rsa.n}\n")
                output.insert(tk.END, f"e = {rsa.e}\n")
                output.insert(tk.END, f"d = {rsa.d}\n")

                # Тест шифрования
                test_msg = "Test"
                encrypted = rsa.encrypt(test_msg)
                decrypted = rsa.decrypt(encrypted)
                output.insert(tk.END, f"\n🧪 Тест: '{test_msg}' → '{decrypted}'\n")
                if test_msg == decrypted:
                    output.insert(tk.END, "✅ Ключи работают!\n")
                else:
                    output.insert(tk.END, "❌ Ошибка ключей!\n")

                self.status.config(text=f"Ключи: {bit} бит")

            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

        btnfr = ttk.Frame(genwin)
        btnfr.pack(pady=5)
        ttk.Button(btnfr, text="Сгенерировать", command=Generate).pack(side="left", padx=10)
        ttk.Button(btnfr, text="Закрыть", command=genwin.destroy).pack(side="left", padx=10)

    # ═══════════════════════════════════════════════════
    # ШИФРОВАНИЕ / РАСШИФРОВАНИЕ (НОВОЕ!)
    # ═══════════════════════════════════════════════════
    def CipherWindow(self):
        # Проверка наличия ключей
        if self.rsa is None:
            messagebox.showwarning("Предупреждение", "Сначала сгенерируйте ключи!\n(Кнопка 'Генерация ключей')")
            return

        cipherwin = tk.Toplevel(self.root)
        cipherwin.title("Шифрование / Расшифрование")
        cipherwin.geometry("600x500")
        cipherwin.grab_set()

        # Переключатель режима
        mode = tk.StringVar(value="encrypt")
        
        modefr = ttk.Frame(cipherwin)
        modefr.pack(pady=10)
        ttk.Radiobutton(modefr, text="🔐 Шифрование", variable=mode, value="encrypt").pack(side="left", padx=20)
        ttk.Radiobutton(modefr, text="🔓 Расшифрование", variable=mode, value="decrypt").pack(side="left", padx=20)

        # Поле ввода текста
        ttk.Label(cipherwin, text="Входные данные:").pack(pady=(10, 2))
        input_text = tk.Text(cipherwin, height=6, width=60)
        input_text.pack(pady=5)
        input_text.insert("1.0", "Введите текст для шифрования...")

        # Поле вывода
        ttk.Label(cipherwin, text="Результат:").pack(pady=(10, 2))
        output_text = tk.Text(cipherwin, height=6, width=60)
        output_text.pack(pady=5)
        output_text.config(state="disabled")

        def process():
            try:
                data = input_text.get("1.0", tk.END).strip()
                if not data or data == "Введите текст для шифрования...":
                    messagebox.showwarning("Предупреждение", "Введите данные!")
                    return

                output_text.config(state="normal")
                output_text.delete("1.0", tk.END)

                if mode.get() == "encrypt":
                    # Шифрование
                    encrypted = self.rsa.encrypt(data)
                    # Показываем как список чисел
                    output_text.insert("1.0", f"Зашифровано:\n{encrypted}\n\n")
                    # Можно сохранить в буфер
                    output_text.insert(tk.END, f"Кол-во символов: {len(data)}\n")
                    output_text.insert(tk.END, f"Модуль n: {self.rsa.n}")
                else:
                    # Расшифрование
                    # Ожидаем формат: [число, число, ...]
                    import ast
                    try:
                        cipher_list = ast.literal_eval(data)
                        if not isinstance(cipher_list, list):
                            raise ValueError("Ожидается список чисел")
                    except:
                        # Пробуем распарсить по-другому
                        cipher_list = [int(x.strip()) for x in data.replace("[", "").replace("]", "").split(",")]

                    decrypted = self.rsa.decrypt(cipher_list)
                    output_text.insert("1.0", f"Расшифровано:\n{decrypted}\n\n")
                    output_text.insert(tk.END, f"Кол-во символов: {len(decrypted)}")

                output_text.config(state="disabled")

            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
                output_text.config(state="disabled")

        def clear_input():
            input_text.delete("1.0", tk.END)
            input_text.insert("1.0", "Введите текст для шифрования...")

        def copy_output():
            result = output_text.get("1.0", tk.END).strip()
            cipherwin.clipboard_clear()
            cipherwin.clipboard_append(result)
            messagebox.showinfo("Буфер", "Скопировано!")

        # Кнопки
        btnfr = ttk.Frame(cipherwin)
        btnfr.pack(pady=15)
        ttk.Button(btnfr, text="Выполнить", command=process).pack(side="left", padx=10)
        ttk.Button(btnfr, text="Очистить", command=clear_input).pack(side="left", padx=10)
        ttk.Button(btnfr, text="Копировать", command=copy_output).pack(side="left", padx=10)
        ttk.Button(btnfr, text="Закрыть", command=cipherwin.destroy).pack(side="left", padx=10)

    # ═══════════════════════════════════════════════════
    # ГРАФИКИ
    # ═══════════════════════════════════════════════════
    def GraphWindow(self):
        if self.res is None:
            messagebox.showwarning("Предупреждение", "Сначала выполните эксперимент!")
            return

        graphwin = tk.Toplevel(self.root)
        graphwin.title("Графики")
        graphwin.geometry("300x250")

        ttk.Label(graphwin, text="Выберите график:").pack(pady=10)

        ttk.Button(graphwin, text="📊 Среднее время", 
                   command=lambda: Graph.PlotRes(self.res)).pack(pady=5, fill="x", padx=20)

        ttk.Button(graphwin, text="📈 Все эксперименты", 
                   command=lambda: Graph.PlotExperiments(self.res)).pack(pady=5, fill="x", padx=20)

        if self.rsa is not None:
            ttk.Button(graphwin, text="⏱️ Атака по времени", 
                       command=lambda: Graph.PlotTimingAttack({"n": self.rsa.n, "e": self.rsa.e, "d": self.rsa.d})).pack(pady=5, fill="x", padx=20)
        else:
            ttk.Button(graphwin, text="⏱️ Атака по времени (недоступно)", 
                       state="disabled").pack(pady=5, fill="x", padx=20)

        ttk.Button(graphwin, text="Закрыть", command=graphwin.destroy).pack(pady=10)


def run_app():
    root = tk.Tk()
    app = Gui(root)
    root.mainloop()