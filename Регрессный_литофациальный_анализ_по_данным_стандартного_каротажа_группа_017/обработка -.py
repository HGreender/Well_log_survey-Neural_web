
import pandas as pd
import lasio

# загрузка данных из файлов LAS
PS = lasio.read('PS.LAS')
PZ = lasio.read('PZ.LAS')
GK = lasio.read('GK.LAS')
NGK = lasio.read('NGK.LAS')
DS = lasio.read('DS.LAS')

# создаем единый csv-файл с данными для создания единой колонки "DEPT"
dept = PS['DEPT'], PS['PS'], PZ['DEPT'], PZ['PZ'], GK['DEPT'], GK['GK'], NGK['DEPT'], NGK['NGK'], DS['DEPT'], DS['DS']
dept_df = pd.DataFrame(dept).T
dept_df.columns = ['DEPT_PS', 'PS', 'DEPT_PZ', 'PZ', 'DEPT_GK', 'GK', 'DEPT_NGK', 'NGK', 'DEPT_DS', 'DS']

# получение списка всех столбцов с глубинами
depth_cols = [col for col in dept_df.columns if col.startswith('DEPT_')]

# объединение всех столбцов с глубинами в один столбец
depths = pd.concat([dept_df[col] for col in depth_cols], ignore_index=True)

# удаление дубликатов и сортировка значений глубин
depths = depths.drop_duplicates().sort_values()

# создание нового DataFrame с общими глубинами
DEPT_df = pd.DataFrame({'DEPT': depths})

# создаем DataFrame для КС
ps = PS['DEPT'], PS['PS']
ps_df = pd.DataFrame(ps).T
ps_df.columns = ['DEPT', 'PS']
# создаем DataFrame для ПС
pz = PZ['DEPT'], PZ['PZ']
pz_df = pd.DataFrame(pz).T
pz_df.columns = ['DEPT', 'PZ']
# создаем DataFrame для ГК
gk = GK['DEPT'], GK['GK']
gk_df = pd.DataFrame(gk).T
gk_df.columns = ['DEPT', 'GK']
# создаем DataFrame для НГК
ngk = NGK['DEPT'], NGK['NGK']
ngk_df = pd.DataFrame(ngk).T
ngk_df.columns = ['DEPT', 'NGK']
# создаем DataFrame для кавернометрии
ds = DS['DEPT'], DS['DS']
ds_df = pd.DataFrame(ds).T
ds_df.columns = ['DEPT', 'DS']

# # Сдвиг данных построчно
# df2['PS'] = df2['PS'].shift(1)
# df2['PZ'] = df2['PZ'].shift(1)
gk_df['DEPT'] = gk_df['DEPT'] - 0.1
ngk_df['DEPT'] = ngk_df['DEPT'] - 0.1
# df2['DS'] = df2['DS'].shift(-1)

# Объединяем все DataFrame'ы по столбцу DEPT
merged_df1 = pd.merge(DEPT_df, ps_df, on='DEPT', how='left')
merged_df2 = pd.merge(merged_df1, pz_df, on='DEPT', how='left')
merged_df3 = pd.merge(merged_df2, gk_df, on='DEPT', how='left')
merged_df4 = pd.merge(merged_df3, ngk_df, on='DEPT', how='left')
merged_df = pd.merge(merged_df4, ds_df, on='DEPT', how='left')

import glob
files = glob.glob('*.xls')
df1 = pd.read_excel(files[0])
df2 = merged_df
df1 = df1.rename(columns={'ИНД_ЛИТ': 'LIT1', 'КР_СЛ':'UP', 'ПД_СЛ':'DOWN'})

# Создаем новый столбец 'характеристика' во второй таблице
df2['LIT'] = ''

# Проходим по каждой строке во второй таблице
for index, row in df1.iterrows():
    # Получаем значение 'DEPT' для текущей строки
    up = row['UP']
    down = row['DOWN']
    lit = row['LIT1']
    # Получаем индексы значений 'DEPT' по условию:
    result = df2.query('DEPT >= @up and DEPT <= @down')
    row_index = result.index
    df2.loc[row_index, 'LIT'] = lit

# # Сдвиг данных построчно
# df2['PS'] = df2['PS'].shift(1)
# df2['PZ'] = df2['PZ'].shift(1)
# df2['GK'] = df2['GK'].shift(1)
# df2['NGK'] = df2['NGK'].shift(1)
# df2['DS'] = df2['DS'].shift(-1)

# Удаляем строки с пустыми значениями
for index, row in df2.iterrows():
    if row['LIT'] == '':
        df2 = df2.drop(index)

cut = df2.dropna(axis=0, how='any', subset=['DEPT', 'PS', 'PZ', 'GK', 'NGK', 'DS', 'LIT'])
print(df2)

# # Сохраняем итоговую таблицу
# cut.to_csv('{}.csv'.format(df1.loc[1,'N_СКВ']), index=False)

# merged_df.to_csv('df1.csv')

# # Модуль для вывода таблицы в excel (Для проверки)
# from openpyxl import Workbook
#
# wb = Workbook()
# ws = wb.active
#
# # запись заголовков столбцов
# ws.cell(row=1, column=1, value='DEPT')
# for i, col in enumerate(['PS', 'PZ', 'GK', 'NGK', 'DS', 'LIT']):
#     ws.cell(row=1, column=i+2, value=col)
#
# # запись данных
# for i, row in merged_df.iterrows():
#     ws.cell(row=i+2, column=1, value=row['DEPT'])
#     for j, col in enumerate(['PS', 'PZ', 'GK', 'NGK', 'DS', 'LIT']):
#         ws.cell(row=i+2, column=j+2, value=row[col])
# wb.save('new_file1.xlsx')





