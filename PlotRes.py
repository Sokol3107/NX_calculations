import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import pickle
import random


def plot2D(start, step):
    with open(r'C:\Users\Алексей\Desktop\Python\NX\allres.pickle', 'rb') as file:
        dat = pickle.load(file)
    for i in range(len(dat)):  # Подготовка данных (приведение первых точек графиков к 0)
        k = dat[i][0]
        for j in range(len(dat[i])):
            dat[i][j] -= k
    n = 0
    fig = plt.figure(figsize=(12, 8))
    for i in dat:
        n += 1
        col = random.choice(list(colors.CSS4_COLORS.keys()))
        max_d = max(i) - min(i)
        plt.plot(i, label='V = ' + str(round(start + step * (n - 1), 2)) + '  d= ' + str(round(max_d, 2)),
                 c=col,figure=fig)
        plt.axhline(max(i), color=col, linestyle='--', linewidth=1)
        plt.axhline(min(i), color=col, linestyle='--', linewidth=1)
    plt.grid(True)
    plt.xlabel('Pos of RD')
    plt.ylabel('Delta, mm')
    plt.legend()
    plt.show()


def plot3D(start, step):
    with open(r'C:\Users\Алексей\Desktop\Python\NX\allres.pickle', 'rb') as file:
        dat = pickle.load(file)
    for i in range(len(dat)):  # Подготовка данных (приведение первых точек графиков к 0)
        k = dat[i][0]
        for j in range(len(dat[i])):
            dat[i][j] -= k
    n = 0
    fig = plt.figure(figsize=(12, 8))
    for i in dat:
        n += 1
        col = random.choice(list(colors.CSS4_COLORS.keys()))
        plt.plot(i, label='Var = ' + str(round(start + step * (n - 1), 2)),
                 c=col,
                 figure=fig)

    plt.grid(True)
    plt.xlabel('Pos of RD')
    plt.ylabel('Delta, mm')
    plt.legend()
    plt.show()


def plotOpt():
    with open(r'C:\Users\Алексей\Desktop\Python\NX\OptRes.pickle', 'rb') as file:  # Загрузка резултататов
        dat = pickle.load(file)
    with open(r'C:\Users\Алексей\Desktop\Python\NX\OptVar.pickle', 'rb') as file:  # Label Var
        Var_dat = pickle.load(file)
    with open(r'C:\Users\Алексей\Desktop\Python\NX\VariableObj.pickle', 'rb') as file:  # Чтение переменных
        VariableObj = pickle.load(file)

    color = list(colors.TABLEAU_COLORS.values())    # Список цветов
    random.shuffle(color)

    fig, ax = plt.subplots(2, 1)  # Создает фигуру с двумя графиками
    ax0, = ax[0].plot(dat, c=color.pop())  # Задает данные первого графика

    title = 'Min = ' + str(round(dat[-1], 2))
    ax1 = []

    for i in range(len(VariableObj)):  # Создает данные второо графика
        title += ' ' + str(VariableObj[i] + ' = ' + str(round(Var_dat[-1][i], 2)))
        ax1.append(ax[1].plot([j[i] for j in Var_dat], c=color.pop()))
    fig.legend([ax0], ['Delta'], 'upper left')
    ax1_lst = [i[0] for i in ax1]
    fig.legend(ax1_lst, VariableObj, 'lower left')
    plt.xlabel('Iteration')
    ax[0].set_title(title)
    ax[0].grid(True)
    ax[1].grid(True)
    plt.grid(True)
    plt.show()
