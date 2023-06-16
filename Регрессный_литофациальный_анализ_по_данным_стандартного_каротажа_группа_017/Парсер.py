import pandas as pd
import lasio
import glob
from sklearn.preprocessing import MinMaxScaler
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

# создание DataFrame для каждого метода
ps = PS['DEPT'], PS['PS']
ps_df = pd.DataFrame(ps).T
ps_df.columns = ['DEPT', 'PS']
pz = PZ['DEPT'], PZ['PZ']
pz_df = pd.DataFrame(pz).T
pz_df.columns = ['DEPT', 'PZ']
gk = GK['DEPT'], GK['GK']
gk_df = pd.DataFrame(gk).T
gk_df.columns = ['DEPT', 'GK']
ngk = NGK['DEPT'], NGK['NGK']
ngk_df = pd.DataFrame(ngk).T
ngk_df.columns = ['DEPT', 'NGK']
ds = DS['DEPT'], DS['DS']
ds_df = pd.DataFrame(ds).T
ds_df.columns = ['DEPT', 'DS']

# Объединяем все DataFrame'ы по столбцу DEPT
merged_df1 = pd.merge(DEPT_df, ps_df, on='DEPT', how='left')
merged_df2 = pd.merge(merged_df1, pz_df, on='DEPT', how='left')
merged_df3 = pd.merge(merged_df2, gk_df, on='DEPT', how='left')
merged_df4 = pd.merge(merged_df3, ngk_df, on='DEPT', how='left')
merged_df = pd.merge(merged_df4, ds_df, on='DEPT', how='left')

# Удаляем строки, в которых все значения NaN
cut = merged_df.dropna(axis=0, how='any', subset=['DEPT', 'PS', 'PZ', 'GK', 'NGK', 'DS'])
# Загрузка xls-файла, который содержит литологические индексы для интервалов глубин
files = glob.glob('*.xls')
df1 = pd.read_excel(files[0])
df2 = pd.DataFrame(cut)
df1 = df1.rename(columns={'ИНД_ЛИТ': 'LIT1', 'КР_СЛ':'UP', 'ПД_СЛ':'DOWN'})

# Создание нового столбца 'LIT' во втором DataFrame
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
# Удаляем строки с пустыми значениями 'LIT'
for index, row in df2.iterrows():
    if row['LIT'] == '':
        df2 = df2.drop(index)

print(df2)
scaler = MinMaxScaler()
df2[['PZ']] = scaler.fit_transform(df2[['PZ']])
print(df2[['PZ']].values)

# # Сохраняем итоговую таблицу
# df2.to_csv('{}.csv'.format(df1.loc[1,'N_СКВ']), index=False)