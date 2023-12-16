from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import r2_score, mean_absolute_percentage_error, mean_squared_error, mean_absolute_error


df = pd.read_csv(r'res.csv', sep=",", decimal='.', skipinitialspace=True)
# целевая переменная
y = df.groupby('session_date')['payer'].sum().reset_index()['payer']
# количество дневных заходов по рекламным каналам
x = df.groupby(['session_date', 'channel'])['user_id'].count().reset_index()
# замена рекламных каналов на процент платящих пользователей по каналам
pro = {'социальные сети': 0.306, 'organic': 0.254, 'реклама у блогеров': 0.293, 'контекстная реклама': 0.264, 'email-рассылки': 0.261}
x['weigth'] = x['channel'].apply(lambda t: pro[t])
# соотношение рекламных каналов
x['user_id'] = x['user_id'] * x['weigth']
x = x.groupby('session_date')['user_id'].sum().reset_index()['user_id']

df_merged = pd.DataFrame({'channel': x, 'sum_buy': y})
# СТРОИМ МОДЕЛЬ
x = pd.DataFrame()
x['channel'] = df_merged['channel']
y = df_merged['sum_buy']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.15, random_state=42)
ohe = OneHotEncoder(sparse_output=False, drop='first', handle_unknown='ignore')
ohe.fit(x_train[['channel']])


def get_ohe(x, cat1):
    temp_df = pd.DataFrame(data=ohe.transform(x[[cat1]]), columns=ohe.get_feature_names_out())
    data = pd.concat([x.reset_index(drop=True), temp_df], axis=1)
    data = data.drop(columns=[cat1], axis=1)
    return data


x_train_new = get_ohe(x_train, "channel")
x_test_new = get_ohe(x_test, "channel")

lin_regr = LinearRegression()
lin_regr.fit(x_train_new, y_train)
predict = lin_regr.predict(x_test_new)
predict = [round(i) for i in predict]
# ПРЕДСКАЗАНИЕ
print(predict)
# анализ ошибок
r2_score = round(r2_score(y_test, predict), 2)
MAPE = round(mean_absolute_percentage_error(y_test, predict) * 100, 2)
MAE = round(mean_absolute_error(y_test, predict), 2)
MSE = round(mean_squared_error(y_test, predict), 2)
RMSE = round(mean_squared_error(y_test, predict) ** 0.5, 2)
print('r2_score =', r2_score) #разница между выборками в наборе данных и прогнозами, сделанными моделью.
print('MAPE =', MAPE) #Средняя абсолютная процентная ошибка
print('MAE =', MAE) #абсолютная ошибку — то, насколько спрогнозированное число разошлось с фактическим числом
print('MSE =', MSE) # оценка среднего значения квадрата ошибок
print('RMSE =', RMSE) #среднее квадратичное различий между прогнозами




















#Index(['user_id', 'region', 'device', 'channel', 'session_start',
#      'session_end', 'sessiondurationsec', 'session_date', 'month', 'day',
#      'hour_of_day', 'order_dt', 'revenue', 'payment_type', 'promo_code']

