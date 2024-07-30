import psutil
import time
import sqlite3
from datetime import datetime
import pygetwindow as gw

# Создаем или подключаемся к базе данных
conn = sqlite3.connect(r'C:\Users\New\PycharmProjects\tracker\activity_tracker.db')
c = conn.cursor()

# Создаем таблицу для хранения данных
c.execute('''CREATE TABLE IF NOT EXISTS activity_log (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 application TEXT,
                 start_time TEXT,
                 end_time TEXT)''')

def get_active_window():
    try:
        window = gw.getActiveWindow()
        if window:
            return window.title
    except:
        return None
    return None

def log_activity(application, start_time, end_time):
    c.execute("INSERT INTO activity_log (application, start_time, end_time) VALUES (?, ?, ?)",
              (application, start_time, end_time))
    conn.commit()

current_app = None
start_time = None

try:
    while True:
        active_app = get_active_window()
        if active_app != current_app:
            if current_app:
                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log_activity(current_app, start_time, end_time)
            current_app = active_app
            start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time.sleep(5)  # Проверяем каждые 5 секунд
except KeyboardInterrupt:
    if current_app:
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_activity(current_app, start_time, end_time)
    conn.close()