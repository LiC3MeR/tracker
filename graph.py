import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Подключаемся к базе данных
conn = sqlite3.connect('activity_tracker.db')
c = conn.cursor()

# Загружаем данные в DataFrame
df = pd.read_sql_query("SELECT * FROM activity_log", conn)

# Преобразуем временные строки в datetime объекты
df['start_time'] = pd.to_datetime(df['start_time'])
df['end_time'] = pd.to_datetime(df['end_time'])

# Рассчитываем длительность
df['duration'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 60  # в минутах

# Группируем данные по приложениям
app_usage = df.groupby('application')['duration'].sum().reset_index()

# Создаем график
plt.figure(figsize=(10, 6))
plt.barh(app_usage['application'], app_usage['duration'], color='skyblue')
plt.xlabel('Duration (minutes)')
plt.ylabel('Application')
plt.title('Application Usage Duration')
plt.show()
