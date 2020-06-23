import sys
import pickle
from scipy.optimize import minimize
import numpy as np


def exchange_data(Var):
    """Отправляет Var в родительский процесс. Возвращает список, содержащий ответы"""
    with open(r'C:\Users\Алексей\Desktop\Python\NX\out.pickle', 'wb') as file:
        if type(Var) is np.ndarray:
            A = Var.tolist()
        else:
            A = Var
        pickle.dump(A, file)
    ResForFileOptVar.append(A)
    sys.stdout.write(str(end).replace('\n', '') + '\n')
    sys.stdout.flush()
    asd = sys.stdin.readline()
    with open(r'C:\Users\Алексей\Desktop\Python\NX\in.pickle', 'rb') as file:
        res = pickle.load(file)
    return res


def prep_data(res):
    """Обрабатывает полученные данные. Возвращает значение оптимизируемой переменной."""
    list_val = []
    for i in range(len(res[0])):
        list_val.append(res[0][i] - res[1][i])  # Собираем все значения разности
    ResForFilePlot.append(list_val)
    delta = abs(max(list_val) - min(list_val))
    ResForFileOpt.append(delta)
    return delta


def f(x):
    res = exchange_data(x)
    return prep_data(res)


def run_calc_for_plot_2D(start_val, end_val, steps_number):
    """Задает Var для построения графика и запускает расчет c одной изменяемой переменной"""
    global end
    if steps_number != 0:
        step = (end_val-start_val)/steps_number
    else:
        step = 0
    for j in [start_val + step*i for i in range(int(steps_number) + 1)]:
        f([j])
    end = 'end'
    print('End of plot')
    with open(r'C:\Users\Алексей\Desktop\Python\NX\allres.pickle', 'wb') as file:  # Запись результатов в файл
        pickle.dump(ResForFilePlot, file)
    import PlotRes
    PlotRes.plot2D(start_val, step)


def run_optimize():
    """Запускает оптимизацию. init_values - список начальных условий для Var"""
    global end
    with open(r'C:\Users\Алексей\Desktop\Python\NX\VariableObj.pickle', 'rb') as file:  # Чтение переменных
        VariableObj = pickle.load(file)

    x0 = np.array([0.0 for i in range(len(VariableObj))])
    res = minimize(f, x0, method='Powell', options={'xtol': 0.1, 'disp': True})
    end = 'end'
    print('Min value = ' + str(round(float(res.fun), 2)) + '\n' + str(res.nfev))

    with open(r'C:\Users\Алексей\Desktop\Python\NX\OptRes.pickle', 'wb') as file:  # Запись результатов в файл
        pickle.dump(ResForFileOpt, file)
    with open(r'C:\Users\Алексей\Desktop\Python\NX\OptVar.pickle', 'wb') as file:  # Запись результатов в файл
        pickle.dump(ResForFileOptVar, file)

    import PlotRes
    PlotRes.plotOpt()


ResForFilePlot = []  # Список для вывода результатов в файл
ResForFileOpt = []  # Список для вывода результатов в файл
ResForFileOptVar = []  # Список для вывода Var в файл
end = 0  # Маркер завершения программы


with open(r'C:\Users\Алексей\Desktop\Python\NX\act.pickle', 'rb') as file:
    act = pickle.load(file)
if act == 'opt':
    run_optimize()  # Запуск оптимизации
else:
    run_calc_for_plot_2D(start_val=0.92, end_val=0.92, steps_number=0)  # Запуск построения графиков


f(['end'])
