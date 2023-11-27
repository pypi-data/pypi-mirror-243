'''
Дисклеймер:
    Данный модуль носит исключительно ознакомительный характер и
    не имеет цели помешать объективной оценки знаний студента.
    Прямая задача этого модуля - хранение большинства примеров решений задач по Терверу и Матстату,
    и быстрый и удобный доступ к ним.
    Всю ответственность за недобросовестное использование модуля носит исключительно сам пользователь и только ОН.

И снова здравствуй дружище! Давно не виделись, как тебе второй курс?
Надеюсь, ты там кайфуешь и веселишься =)
Поблагодарим 808 за предоставленный код
Ave ПЕ!


P.S.
1) Чтобы был хороший и красивый вывод не забудь обернуть в print()
2) Удачи на сессии ;)

P.P.S.
ПОСЛЕ ПРОЧТЕНИЯ СЖЕЧЬ!!!
'''


def vgusibp():
    'В группе учится 29 студентов. Ими были получены'
    print("""import numpy as np
import statistics as stats
from scipy import stats
# Ваши оценки
grades = [90, 79, 53, 62, 66, 68, 75, 0, 82, 29, 0, 29, 68, 90, 0, 60, 44, 44, 70, 68, 70, 89, 0, 68, 0, 66, 0, 59, 70]
# Удаляем нулевые оценки
positive_grades = [grade for grade in grades if grade > 0]
# 1) Средняя положительная оценка (A)
A = np.mean(positive_grades)
print("Средняя положительная оценка (A):", round(A, 2))
# 2) Медиана положительных оценок (M)
M = np.median(positive_grades)
print("Медиана положительных оценок (M):", M)
gr = [g for g in positive_grades if g>=M]
# 3) Среднее гармоническое (H) и среднее геометрическое (G)
H = stats.hmean(gr)
G = stats.gmean(gr)
print("Среднее гармоническое (H):", H)
print("Среднее геометрическое (G):", G)
# 4) Медианная оценка в части группы, где студенты набрали не менее M баллов (Q)
grad = [grade for grade in positive_grades if grade >= M]
Q = np.median(grad)
print("Медианная оценка в части группы с баллами выше либо равными M (Q):", Q)
# 5) Количество студентов с оценками между H и Q (включая границы) (N)
grades_between_H_and_Q = [grade for grade in positive_grades if (grade <= H) and (grade >= Q)]
N = len(grades_between_H_and_Q)
print("Количество студентов с оценками между H и Q (включая границы) (N):", N)""")

def scheunio():
    'Следующие 28 чисел – это умноженные на 10000 и округленные'
    print("""import numpy as np
from scipy import stats
from scipy.integrate import quad

# Преобразованные доходности (ПД)
PD = [-9, 9, -138, -145, 186, 78, 34, -37, -19, -68, -82, 158, 96, -189, 24, 84, -99, 125, -39, 26, 62, -91, 239, -211, 2, 129, 2, -16]

# 1) Среднее арифметическое ПД (μ)
mean_PD = np.mean(PD)

# 2) Эмпирическое стандартное отклонение ПД (σ)
std_dev_PD = np.std(PD, ddof=0)

normal_distribution = stats.norm(loc=mean_PD, scale=std_dev_PD)

# 3) Квартили L и H
L = normal_distribution.ppf(0.25)  # Квартиль L
H = normal_distribution.ppf(0.75)  # Квартиль H

# 4) Количество ПД, попавших в интервал от L до H
count_PD_between_L_and_H = sum(L <= pd <= H for pd in PD)


#5)
# Calculate the cumulative distribution function (CDF) values for the data
sorted_PD = np.sort(PD)
F_hat_x = np.arange(1, len(sorted_PD) + 1) / len(sorted_PD)

# Calculate the CDF values for the normal distribution
F_x = normal_distribution.cdf(sorted_PD)

# Calculate the absolute differences between the two CDFs
differences = np.abs(F_x - F_hat_x)

# Find the maximum absolute difference
max_difference = np.max(differences)


print("Расстояние между функциями F^(x) и F(x):", round(distance, 4))
print("1) Среднее арифметическое ПД (μ):", round(mean_PD, 2))
print("2) Эмпирическое стандартное отклонение ПД (σ):", round(std_dev_PD, 2))
print("3) Квартиль L:", round(L, 2))
print("   Квартиль H:", round(H, 2))
print("4) Количество ПД, попавших в интервал от L до H:", count_PD_between_L_and_H)
print("5) Расстояние между функциями F^(x) и F(x):", round(max_difference, 4))""")


def vguspib():
    'В группе Ω учатся студенты: ω1,...,ω30. Пусть X и Y – 100-балльные экзаменационные оценки (i для того, чтобы обозначить, что Х и У)'
    print("""import numpy as np

# Оценки X и Y
X = np.array([71, 52, 72, 87, 81, 100, 90, 54, 54, 58, 56, 70, 93, 46, 56, 59, 42, 60, 33, 83, 50, 93, 41, 55, 60, 37, 71, 42, 85, 39])
Y = np.array([71, 58, 81, 92, 81, 94, 96, 46, 60, 62, 49, 60, 86, 48, 61, 52, 40, 60, 37, 92, 57, 93, 42, 64, 59, 30, 71, 44, 82, 39])

# Шаг 1: Выбор данных, где X ≥ 50 и Y ≥ 50
mask = (X >= 50) & (Y >= 50)
X_conditional = X[mask]
Y_conditional = Y[mask]

# Шаг 2: Вычисление условного среднего
mean_X_conditional = np.mean(X_conditional)
mean_Y_conditional = np.mean(Y_conditional)

# Шаг 3: Вычисление условных дисперсий
var_X_conditional = np.var(X_conditional, ddof=1)  # Используем ddof=1 для несмещенной дисперсии
var_Y_conditional = np.var(Y_conditional, ddof=1)

# Шаг 4: Расчет условной ковариации и коэффициента корреляции
cov_XY_conditional = np.cov(X_conditional, Y_conditional, ddof=0)[0, 1]  # Ковариация в матрице ковариации
corr_XY_conditional = cov_XY_conditional / (np.sqrt(var_X_conditional) * np.sqrt(var_Y_conditional))

print("Условная ковариация X и Y при X ≥ 50 и Y ≥ 50:", round(cov_XY_conditional, 2))
print("Условный коэффициент корреляции X и Y при X ≥ 50 и Y ≥ 50:", round(corr_XY_conditional, 3))
""")


def psignpu():
    'Поток Ω состоит из k групп: Ω1,...,Ωk, k=3. На потоке учатся '
    print("""k = 3
n = [24, 26, 30]
xi = [70, 76, 77]
sigma = [4, 6, 8]

N = sum(n)

l_1 = []
for i in range(k):
    l_1.append(n[i]*xi[i])
x = 1/N *sum(l_1)
print("Среднее значение:", round(x,3))

l_2 = []
for i in range(k):   
    l_2.append(n[i]*(xi[i]-x)**2)

l_3 = []
for i in range(k):
    l_3.append(sigma[i]**2*n[i])

standart_otkl = (1/N * (sum(l_2) + sum(l_3)))**0.5
print("Стандартное отклонение:", round(standart_otkl, 4))""")



def vguspbo():
    'В группе Ω учатся 27 студентов, Ω={1,2,...,27}. Пусть X(i) – 100-балльная оценка(допускается повторение)'
    print("""import numpy as np

# Оценки в группе
X_group = [100, 86, 51, 100, 95, 100, 12, 61, 0, 0, 12, 86, 0, 52, 62, 76, 91, 91, 62, 91, 65, 91, 9, 83, 67, 58, 56]

# Количество выборок
n_samples = 7

# 1) Дисперсия Var(X¯¯¯¯)
var_X_bar = np.var(X_group) / n_samples

mean_X_group = np.mean(X_group)
moment_3 = np.mean((X_group - mean_X_group) ** 3)/n_samples**2

#centr_mom_x_sr = (np.mean(X_group**3) - 3*np.mean(X_group)*np.mean(X_group**2) + 2*np.mean(X_group)**3)/n**2

print("1) Дисперсия Var(X¯¯¯¯):", round(var_X_bar, 3))
print("2) Центральный момент μ3(X¯¯¯¯):", round(moment_3, 3))""")



def vguspbon():
    'В группе Ω учатся 27 студентов, Ω={1,2,...,27}. Пусть X(i) – 100-балльная оценка( повторение не допускается - n)'
    print("""N = 27 #количество студентов в группе, объем генеральной совокупности
n = 6  #количество выбранных студентов, обхем выборочной совокупности
#бесповторная выборка 

marks = np.array([100, 78, 77, 51, 82, 100, 73, 53, 78, 55, 7, 0, 81, 15, 96, 12, 71, 70, 53, 0, 73, 100, 55, 100, 59, 89, 81]) #оценки в группе

E_x_sr = np.mean(marks)
Var_x_sr = (np.var(marks)/n) * ((N - n)/(N - 1))

print('Математическое ожидание =',round(E_x_sr,3))
print('Дисперсия =',round(Var_x_sr,3))""")



def rbnedpz():
    'Распределение баллов на экзамене до перепроверки задано '
    print("""marks = np.array([2,3,4,5]) #оценка работы
count_works = np.array([7, 48, 8, 105])  #количество работ
teachers = 6
N = np.sum(count_works)   # объем генеральной совокупности
n = N/teachers   # объем выборочной совокупности


mean_mean_x = (count_works@marks)/N
var_mean_x = ((marks**2@count_works)/N - ((count_works@marks)/N)**2) * ((N-n)/(n*(N-1)))

print('Математическое ожидание =',round(mean_mean_x,2))
print('стандартное отклонение =',round(np.sqrt(var_mean_x),3))""")



def dikkisp():
    'Две игральные кости, красная и синяя, подбрасываются'
    print("""n = 19 # количество различных комбинаций 
a = 11 #коэффициент перед R в случайной велечине X
b = -9  #коэффициент перед B в случайной велечине X

red = [1, 2, 3, 4, 5, 6]
blue = [1, 2, 3, 4, 5, 6]

E_r = np.mean(red)
Var_r = np.var(red)
E_b = np.mean(blue)
Var_b = np.var(blue)

N = 36


mean_mean_x = a*E_r + b*E_b
var_mean_x = (a**2*var_r + b**2*var_b)*(((N-n)/(n*(N-1))))

print('Математическое ожидание =',round(mean_mean_x,2))
print('стандартное отклонение =',round(np.sqrt(var_mean_x),3))""")



def ipmmpdt():
    'Имеется 11 пронумерованных монет. Монеты подбрасываются до тех '
    print("""n = 11 # количество пронумеронованных монет в броске
m = 257 # количество различных комбинаций орел-решка

#количество орлов в броске распределено по биноминальному закону ==> E(X) = np
p=1/2
N = 2**n # количество различных вариантов бросков --> генереальная совокпность 

mean_mean_x = n*p
var_mean_x = (n*p*(1-p)) * (((N - m)/( m*(N-1))))

print('Математическое ожидание =',round(mean_mean_x,2))
print('стандартное отклонение =',round(var_mean_x,3))""")



def erpmdkk():
    'Эмпирическое распределение признаков (1) математическое ожидание E(X¯¯¯¯); 2) дисперсию Var(Y¯¯¯¯); 3) коэффициент корреляции ρ(X¯¯¯¯,Y¯¯¯¯).)'
    print("""N = 100 #генеральная совокупность 
n = 7 #бесповторная вбыорка
X = np.array([100,400]) 
Y = np.array([1,2,3])
XY = np.array([[11,32,11],[24,11,11]])


X_n = np.array([np.sum(row) for row in XY])
Y_n = np.array([np.sum(row) for row in np.transpose(XY)])

x_mean = X_n@X/np.sum(X_n)
y_mean = Y_n@Y/np.sum(Y_n)

var_x_mean = ((X**2@X_n)/np.sum(X_n) - (X_n@X/np.sum(X_n))**2 ) * (((N-n)/(n*(N-1))))
var_y_mean = ((Y**2@Y_n)/np.sum(Y_n) - (Y_n@Y/np.sum(Y_n))**2 ) * (((N-n)/(n*(N-1))))

cov_x_y = np.sum([(X[i] - x_mean)*np.sum([(Y[j] - y_mean) * XY[i][j] for j in range(len(Y))]) for i in range(len(X)) ])/N * (((N-n)/(n*(N-1))))

p = cov_x_y  / np.sqrt((var_x_mean*var_y_mean))

print('математическое ожидание X_mean =',round(x_mean,3))
print('дисперсия Y_mean =',round(var_y_mean,3))
print('коэффициент корреляции =',round(p,3))""")



def erpmsok():
    'Эмпирическое распределение признаков (1) математическое ожидание E(X¯¯¯¯); 2) дисперсию Var(Y¯¯¯¯); 3) коэффициент корреляции ρ(X¯¯¯¯,Y¯¯¯¯).)'
    print("""N = 100 #генеральная совокупность 
n = 6 #бесповторная вбыорка
X = np.array([100,300]) 
Y = np.array([1,2,4])
XY = np.array([[21,17,12],[10,27,13]])


X_n = np.array([np.sum(row) for row in XY])
Y_n = np.array([np.sum(row) for row in np.transpose(XY)])

x_mean = X_n@X/np.sum(X_n)
y_mean = Y_n@Y/np.sum(Y_n)

var_x_mean = ((X**2@X_n)/np.sum(X_n) - (X_n@X/np.sum(X_n))**2 ) * (((N-n)/(n*(N-1))))
var_y_mean = ((Y**2@Y_n)/np.sum(Y_n) - (Y_n@Y/np.sum(Y_n))**2 ) * (((N-n)/(n*(N-1))))

cov_x_y = np.sum([(X[i] - x_mean)*np.sum([(Y[j] - y_mean) * XY[i][j] for j in range(len(Y))]) for i in range(len(X)) ])/N * (((N-n)/(n*(N-1))))


print('математическое ожидание X_mean =',round(y_mean,4))
print('дисперсия Y_mean =',round(np.sqrt(var_x_mean),3))
print('ковариация=',round(cov_x_y,3))""")
