import pandas as pd


df = pd.read_csv(r'YL.csv', sep=",", decimal='.', skipinitialspace=True)
#PEP8
df.columns = [i.lower().replace(" ", "_") for i in df.columns]
#Добавление нуля в часы к шкалам со временем
def zero(x):
    if x != 'nan':
        if len(x.split()[1]) == 7:
            a, b = x.split()[0], x.split()[1]
            b = f'0{b}'
            c = a + b
            x = c
    return pd.to_datetime(x)

#изменяем временные шкалы
df['session_start'] = df['session_start'].apply(lambda x: zero(x))
df['session_end'] = df['session_end'].apply(lambda x: zero(x))
df['order_dt'] = df['order_dt'].astype(str)
df['order_dt'] = df['order_dt'].apply(lambda x: zero(x))
#округление миллисекунд до секунд
df['sessiondurationsec'] = df['sessiondurationsec'].apply(lambda x: pd.to_datetime(round(x)))

# число явных дубликатов и их удаление
i_see_it = len(df) - len(df.drop_duplicates())
#print(i_see_it) -> 3
df = df.drop_duplicates()
# неявные дубликаты
a = df[df.columns[4:]]
double = len(a) - len(a.drop_duplicates())
# double = 0, следовательно неявных дубликатов не обнаружено
# заполнение пропусков
stupid_nans = df.groupby(['month'])['region']
df['region'].fillna(lambda x: stupid_nans[x])
stupid_nans = df.groupby(['month'])['device']
df['device'].fillna(lambda x: stupid_nans[x])
stupid_nans = df.groupby(['month'])['channel']
df['channel'].fillna(lambda x: stupid_nans[x])
# print(len(df) - len(df.drop_duplicates())) -> 0 внезапные дубликаты не объявились)


