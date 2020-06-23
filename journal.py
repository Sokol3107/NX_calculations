import math
import NXOpen
import NXOpen.Preferences
import subprocess
import pickle
import sys
import time


def printNX(string):
    global theSession
    theSession.ListingWindow.Open()
    theSession.ListingWindow.WriteLine(str(string))


def update():
    """Обновление модели"""
    global theSession
    markId5 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "NX update")
    nErrs1 = theSession.UpdateManager.DoUpdate(markId5)


def FindObj(Name):
    global workPart
    return workPart.Expressions.FindObject(Name)


def calc(Var):
    """Функция производит расчет в NX со значениями переменных, переданных в списке Var.
     Возвращает кортеж с двумя списками результатов."""
    for i in range(len(Var)):
        FindObj(VariableObj[i]).Value = float(Var[i])
        update()
    CurVal = InpObj_init
    Out = [[],[]]
    for i in range(Speeds):
        for j in range(len(InpObjNames)):
            FindObj(InpObjNames[j]).Value = InpObjVals[j][i]
        update()
        Out[0].append(FindObj(OutObj[0]).Value)
        Out[1].append(FindObj(OutObj[1]).Value)

    return Out


def start_calculation():
    """Запускает процесс расчета, осуществляет связь с подпроцессом, использующим библиотеки Python"""
    end = 0    # Определяет конец субпроцесса

    sub = subprocess.Popen([r'C:\Program Files\Python36\python.exe', r'C:\Users\Алексей\Desktop\Python\NX\OptimizationNX.py'],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             universal_newlines=True)
    while True:
        cur_time = time.time()
        end = str(sub.stdout.readline().rstrip('\n'))
        if end != '0':
            n = 0
            while n < 15:
                end = str(sub.stdout.readline().rstrip('\n'))
                if end.startswith('end'):
                    break
                printNX(end)
                n += 1
            printNX('Time: ' + str(round((cur_time - start_time)/60, 2)) + ' min')
            break
        with open(r'C:\Users\Алексей\Desktop\Python\NX\out.pickle', 'rb') as f:
            V = pickle.load(f)
        res = calc(V)
        with open(r'C:\Users\Алексей\Desktop\Python\NX\in.pickle', 'wb') as f:
            pickle.dump(res, f)
        sub.stdin.write('123\n')
        sub.stdin.flush()


start_time = time.time()
theSession = NXOpen.Session.GetSession()
workPart = theSession.Parts.Work

InpObj_init = 0.0  # Начальное значение задающей переменной InpObj
CassetteWidth = 36.5  # Ширина кассеты
Speeds = 10
InpObjNames = ['Pos_LT', 'Pos_820']  # Переменные, задающие перемещение переключателя
InpObjVals = [[i*CassetteWidth/(Speeds - 1) for i in range(Speeds)],  # Значения переменных InpObjNames
              [-0.144, 3.766, 7.703, 11.648, 15.596, 19.545, 23.494, 27.441, 31.386, 35.325]]  # Pos 820
              # [-0.2, 3.65, 7.5, 11.3, 15.1, 18.9, 22.7, 26.5, 30.3, 34.1, 37.7]]  # Pos_9000
VariableObj = ['X_Pos', 'Y_Pos', 'Z_Pos']  # Список оптимизируемых переменных
OutObj = ['Meas_820', "Meas_LT"]  # Измеряемые переменные
act = 'plot'  # Выбор решения ('opt' - отимизация, 'plot' - построение графиков)

with open(r'C:\Users\Алексей\Desktop\Python\NX\VariableObj.pickle', 'wb') as file:
    pickle.dump(VariableObj, file)
with open(r'C:\Users\Алексей\Desktop\Python\NX\act.pickle', 'wb') as file:
    pickle.dump(act, file)


start_calculation()

