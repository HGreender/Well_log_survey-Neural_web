import pandas as pd


df2 = pd.read_csv('learning_train.csv', delimiter=',', encoding='UTF-8')

df = df2.sample(frac=0.1)

print(df2)
print(df)

# Сохраняем итоговую таблицу
df.to_csv('{}.csv'.format('TEST_BEST'), index=False)
print('Сохранение завершено\n')