import pandas as pd
from scipy.stats import shapiro, f_oneway, kruskal


df = pd.read_csv(r'res.csv', sep=",", decimal='.', skipinitialspace=True)

# ПРОВЕРКА ГИПОТЕЗ

days_purchases = df.groupby('day')['payer'].sum()
region_device = df.groupby(['region', 'device'])['payer'].sum()
if ((shapiro(days_purchases)[1] >= 0.05) and (shapiro(region_device)[1] >= 0.05)):
    r = round(f_oneway(days_purchases, region_device)[1], 4)
    #print(r)
    # p-value меньше 0.05 - взаимосвязь между типом устройства и кол-вом покупок в день есть
else:
    k = round(kruskal(days_purchases, region_device)[1], 4)
    print(k)
    # p-value меньше 0.05 - взаимосвязь между типом устройства и кол-вом покупок в день есть


region_channel = df.groupby(['region', 'channel'])['payer'].sum()
if ((shapiro(days_purchases)[1] >= 0.05) and (shapiro(region_channel)[1] >= 0.05)):
    r = round(f_oneway(days_purchases, region_channel)[1], 4)
    #print(r)
    # p-value меньше 0.05 - взаимосвязь между рекламным каналом и кол-вом покупок в день есть
else:
    k = round(kruskal(days_purchases, region_channel)[1], 4)
    print(k)
    # p-value меньше 0.05 - взаимосвязь между рекламным каналом и кол-вом покупок в день есть







#Index(['user_id', 'region', 'device', 'channel', 'session_start',
#      'session_end', 'sessiondurationsec', 'session_date', 'month', 'day',
#      'hour_of_day', 'order_dt', 'revenue', 'payment_type', 'promo_code']

