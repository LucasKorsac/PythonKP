#Graph - графическое представление

import matplotlib.pyplot as plt

# Среднее время взлома
def PlotRes(df):
    plt.figure()
    for val, group in df.groupby("c"):
        grouped = group.groupby("bit")["time"].mean()
        plt.plot(grouped.index, grouped.values, marker="o", label=f"Близкие простые: {val}")
    plt.xlabel("Размер ключа")
    plt.ylabel("Среднее время взлома")
    plt.title("Атака RSA - среднее время")
    plt.legend()
    plt.grid(True)
    plt.show()

# Распределение времени всех экспериментов
def PlotExperiments(df):
    plt.figure(figsize=(8, 5))

    colors = {True: "#4f3663", False: "#366340"}
    lbl = set()

    for val in [False, True]:
        group = df[df["c"] == val].reset_index(drop=True)
        groupst = group.sort_values("bit").reset_index(drop=True)

        label = f"Эксперимент: {val}" if val not in lbl else None
        lbl.add(val)

        plt.scatter(groupst["time"], groupst["bit"],
                    color=colors[val], s=90, label=label)

        # Подписи НАД точками
        for idx, (x, y) in enumerate(zip(groupst["time"], groupst["bit"]), 1):
            plt.text(x, y + 0.2, str(idx),  # Смещение вверх
                     fontsize=12,         # Размер шрифта
                     #fontweight='bold',
                     ha='center', va='bottom')

    plt.ylabel("Размер ключа")
    plt.xlabel("Время взлома (сек)")
    plt.title("Все эксперименты RSA")
    plt.legend()
    plt.grid(True)
    plt.show()