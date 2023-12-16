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
purchases = df['payer'].sum()
count_of_users = len(df['user_id'].unique())
one_user_mean = round(purchases / count_of_users, 1)

#Средняя продолжительность сессии по рекламным каналам
session_channel = df.groupby(['channel'])['sessiondurationsec'].mean()

#Средняя продолжительность сессии по типу устройства
device_channel = df.groupby(['device'])['sessiondurationsec'].mean()

#ТОП-3 рекламных канала по среднему чеку
top_channel_check = df.groupby(['channel'])['revenue'].apply(lambda x: round(x.mean())
                                                             ).sort_values(ascending=False)[:3]
#ТОП-3 региона по среднему чеку
top_region_check = df.groupby(['region'])['revenue'].apply(lambda x: round(x.mean())
                                                             ).sort_values(ascending=False)[:3]


#ТОП-3 месяца по среднему чеку с разбивкой по регионам
top_region_check_by_regions = df.groupby(['region', 'month'])['revenue'].apply(lambda x: round(x.sum() / len(x))
                                                             ).sort_values(ascending=False)

months = {5: 'май', 6: 'июнь', 7: 'июль', 8: 'август', 9: 'сентябрь', 10: 'октябрь'}
top_region_check_by_regions = top_region_check_by_regions.reset_index()
top_region_check_by_regions['month'] = top_region_check_by_regions['month'].apply(lambda x: months[x])
region_check_by_regions = top_region_check_by_regions.groupby('region').apply(lambda x: x)
region_check_by_regions = region_check_by_regions.drop('region', axis=1).rename(columns={"revenue": "средний_чек"})
#print(region_check_by_regions)
top_region_check_by_regions = top_region_check_by_regions.groupby('region')['revenue'].apply(lambda x: round(x.mean())
                                                             ).sort_values(ascending=False)[:3].reset_index().rename(columns={"revenue": "средний_чек"})
#print(top_region_check_by_regions)


#MAU с разбивкой по рекламным каналам
mau_by_channel = df.groupby(['channel', 'month'])['user_id'].unique().apply(lambda x: len(x)).reset_index()

#ТОП-3 рекламных каналов по количеству уникальных пользователей в месяц
top_mau_by_channel = mau_by_channel.groupby('channel')['user_id'].apply(lambda x: round(x.mean()))
top_mau_by_channel = top_mau_by_channel.sort_values(ascending=False)[:3]
#print(top_mau_by_channel)

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

