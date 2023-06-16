import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Открываем CSV-файл и создаём дата-фрейм
while True:
    try:
        file = str(input('Введите номер скважины: '))
        print()
        df2 = pd.read_csv(file + '.csv', delimiter=',', encoding='UTF-8')
    except Exception: print('Неправильный ввод.')
    else:
        print(f'Принятно.\nЗагружается скважина №{file}')
        break


print(df2)
print('\nМинимальное значение DS:', df2[['DS']].min().values)
print('Индекс минимального значения DS:', df2[['DS']].idxmin().values)
print('\nМаксимальное значение DS:', df2[['DS']].max().values)
print('Индекс максимального значения DS:', df2[['DS']].idxmax().values)

# Альфа-ПС
def alphaPS(*pd):
    ps = pd[0]
    pd_max = ps.max()
    pd_min = ps.min()
    alphaPS = (pd_max - ps) / (pd_max - pd_min)
    return alphaPS
temp = df2[['PS']].values
df2[['PS']] = alphaPS(temp)

# MinMaxScaler для PZ
scaler = MinMaxScaler()
df2[['PZ']] = scaler.fit_transform(df2[['PZ']])
# min = df2[['PZ']].min().values[0]

# Двойной разностный параметр для GK и NGK
def Double_Diff_GK_NGK(*pd):
    pd = pd[0]
    pd_max = pd.max()
    pd_min = pd.min()
    double = (pd - pd_min) / (pd_max - pd_min)
    return double

temp = df2[['GK']].values
df2[['GK']] = Double_Diff_GK_NGK(temp)
temp = df2[['NGK']].values
df2[['NGK']] = Double_Diff_GK_NGK(temp)

#Шкалирование DS
def NormDS(df):
    DS_nom_1 = 0.190
    DS_nom_2 = 0.216
    check = 0
    while check == 0:
        nom = float(input('\nВведите номинальный диаметр скважины: '))
        if nom == DS_nom_1:
            print('Accepted 0.190')
            check = 1
        elif nom == DS_nom_2:
            print('Accepted 0.216')
            check = 2
        elif nom == 3:
            print('Завершение программы...')
            exit()
        else:
            print('ALARMA! Неправильный номинальный диаметр скважины.\n'
                  f'Вы ввели {nom}. Введите 190 либо 216 в зависимости от вашей скважины.\n'
                  f'Введите "3" для выхода из программы')

    df = df - nom   # Центрируем данные. 0 - номинал, отриц. - гл. корочка, положит. - каверны
    df[(df.DS < 0)] = df.query('DS<0') * (-1)
    # df_max = df.max()
    # df_min = df.min()
    # norm = (df_max - df) / (df_max - df_min)
    scaler2 = MinMaxScaler()
    norm = scaler2.fit_transform(df)
    return norm

temp = df2[['DS']]
df2[['DS']] = NormDS(temp)
print(df2)
print('\nМинимальное значение DS:', df2[['DS']].min().values)
print('Индекс минимального значения DS:', df2[['DS']].idxmin().values)
print('\nМаксимальное значение DS:', df2[['DS']].max().values)
print('Индекс максимального значения DS:', df2[['DS']].idxmax().values)