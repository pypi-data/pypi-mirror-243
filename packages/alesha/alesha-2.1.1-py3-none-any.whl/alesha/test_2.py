def max_plaus():
    """Нахождение оценок с помощью метода правдободобия"""
    print("""import numpy as np
    import scipy.integrate as integrate
    sample = np.array(
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 1, 1, 3, 4, 4, 5, 4, 6, 6, 11,
         9, 19, 23, 25, 33, 36, 36, 46, 46, 49, 58, 90, 76, 66, 69, 75, 68, 44, 39, 21, 16, 5, 2, 1, 0, 0, 0])
    percents = []
    for i in range(len(sample)):
        if sample[i] != 0:
            l = [i] * sample[i]
            percents.extend(l)
    percents = np.array(percents) / 100

    def lnL(X, a, b):
        n = X.shape[0]
        return n * np.log(a) + n * np.log(b) + (a - 1) * np.sum(np.log(X)) + (b - 1) * np.sum(np.log(1 - X ** a))

    maxL = -np.inf
    for a in range(1, 21):
        for b in range(1, 21):
            L = lnL(percents, a, b)
            if L > maxL:
                maxL = L
                a_max = a
                b_max = b

    print('A', a_max, 'B', b_max)
    a, b = a_max, b_max

    def f_x(x):
        return a * b * x ** (a - 1) * (1 - x ** a) ** (b - 1)

    def xfx(x):
        return x * f_x(x)

    result = integrate.quad(xfx, 0, 1)[0]
    print('Математическое ожидание', result)

    def F(x):
        return integrate.quad(f_x, 0, x)[0]

    x_val = np.linspace(0, 1, 1000000)
    q = 0.2
    for x in x_val:
        if F(x) >= q:
            print('Квантиль', x)
            break""")


def dov_int():
    """интервальная оценка коэффициента корреляции"""
    print("""import math
    import numpy as np
    from scipy import stats
    x = ('-0,616; -0,238; 0,173; -0,255; 0,531; 0,718; -0,161; 0,371; -1,014; -0,413; -1,571; 0,485; 0,486; 0,688; -0,'
         '944; 0,155; 0,003; 0,111; 0,752; 0,783; -0,102; -0,74; -2,097; 1,349; -0,044; -0,617; -0,782; -0,873; -0,'
         '995; -1,256; -0,596')
    y = ('-1,34; -0,25; 0,101; -0,626; -0,088; 0,539; -0,451; 0,233; -1,186; -0,423; -1,329; 0,231; 0,209; 0,638; -0,'
         '274; -0,491; -0,319; 0,294; 0,895; 1,164; -0,57; -1,078; -1,526; 1,491; 0,182; -0,31; -1,001; -0,969; -0,'
         '918; -0,904; -0,595')
    j = 0.93
    x = [float(i.replace(',', '.')) for i in x.split(';')]
    y = [float(i.replace(',', '.')) for i in y.split(';')]
    p = np.corrcoef(x, y)[0][1]
    z = stats.norm.isf((1 - j) / 2)
    high = math.tanh(math.atanh(p) + 1 / (len(x) - 3) ** 0.5 * z)
    print('Выборочный коэф корреляции', p)
    print('Верхняя граница', high)""")
