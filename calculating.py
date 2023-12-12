import pandas as pd


df = pd.read_csv(r'res.csv', sep=",", decimal='.', skipinitialspace=True)
# корректировка данных на пользователей, совершивших 2 покупки
#print(df[df['payer'] == 1]['user_id'].value_counts().head(5))
df.loc[(909, 'region')] = 'Germany'
df.loc[(909, 'channel')] = 'контекстная реклама'
df.loc[(544, 'device')] = 'Mac'
df.loc[544, 'channel'] = 'organic'
df.loc[(646, 'channel')] = 'email-рассылки'
df.loc[(646, 'region')] = 'France'
df.loc[(542, 'region')] = 'UK'
df.loc[(542, 'device')] = 'Mac'
df.loc[(542, 'channel')] = 'контекстная реклама'
df.loc[(559, 'region')] = 'UK'
df.loc[(559, 'device')] = 'PC'
df.loc[(559, 'channel')] = 'контекстная реклама'

###################################################################################################################
# Средний чек по всем покупателям
all_check = round(df['revenue'].mean())

# Сколько покупок в среднем совершает 1 пользователь?
purchases = len(df['revenue'].dropna())
count_of_users = len(df['user_id'].unique())
one_user_mean = round(count_of_users / purchases, 1)
#Средняя продолжительность сессии по рекламным каналам
session_channel = df.groupby(['channel'])['sessiondurationsec'].sum()

#Средняя продолжительность сессии по типу устройства
device_channel = df.groupby(['device'])['sessiondurationsec'].sum()

#ТОП-3 рекламных канала по среднему чеку
top_channel_check = df.groupby(['channel'])['revenue'].apply(lambda x: round(x.mean())
                                                             ).sort_values(ascending=False)[:3]
#ТОП-3 региона по среднему чеку
top_region_check = df.groupby(['region'])['revenue'].apply(lambda x: round(x.mean())
                                                             ).sort_values(ascending=False)[:3]
#ТОП-3 месяца по среднему чеку с разбивкой по регионам
top_region_check_by_regions = df.groupby(['month', 'region'])['revenue'].apply(lambda x: round(x.mean())
                                                             ).sort_values(ascending=False)
#MAU с разбивкой по рекламным каналам
mau_by_channel = df.groupby(['month', 'channel'])['user_id'].unique().apply(lambda x: len(x))

#ТОП-3 рекламных каналов по количеству уникальных пользователей в месяц
top_mau_by_channel = df.groupby(['month', 'channel'])['user_id'].unique().apply(lambda x: len(x)
                                                                                ).sort_values(ascending=False)[:3]

# ТАБЛИЦА, определяющая какой вид источника принес больше всего платящих пользователей и большую сумму продаж
table = pd.DataFrame()
table['user_id'] = df.groupby('channel')['user_id'].apply(lambda x: len(x))
table['unique_users'] = df.groupby('channel')['user_id'].unique().apply(lambda x: len(x))
table['payer'] = df.groupby('channel')['payer'].sum()
table['revenue'] = df.groupby('channel')['revenue'].sum()
print(table.sort_values(by=['payer', 'revenue'], ascending=False)[:1])






#Index(['user_id', 'region', 'device', 'channel', 'session_start',
#      'session_end', 'sessiondurationsec', 'session_date', 'month', 'day',
#      'hour_of_day', 'order_dt', 'revenue', 'payment_type', 'promo_code']

