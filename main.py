import os
import time
from datetime import datetime
from PIL import ImageGrab
from pynput import mouse, keyboard
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Настройка базы данных
DATABASE_URL = r'sqlite:///C:\Users\New\PycharmProjects\tracker\activity_tracker.db'
engine = sa.create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = sa.orm.declarative_base()

# Определение модели для хранения данных
class ActivityLog(Base):
    __tablename__ = 'activity_log'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    timestamp = sa.Column(sa.DateTime, default=datetime.utcnow)
    screenshot_path = sa.Column(sa.String)
    keyboard_activity_count = sa.Column(sa.Integer, default=0)
    mouse_activity_count = sa.Column(sa.Integer, default=0)

Base.metadata.create_all(engine)

# Настройка директорий
BASE_DIR = r'C:\Users\New\PycharmProjects\tracker'
SCREENSHOT_DIR = os.path.join(BASE_DIR, 'static', 'screenshots')
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

keyboard_activity_count = 0
mouse_activity_count = 0

def on_press(key):
    global keyboard_activity_count
    keyboard_activity_count += 1
    print(f"Key pressed: {key}")

def on_click(x, y, button, pressed):
    global mouse_activity_count
    if pressed:
        mouse_activity_count += 1
    print(f"Mouse {'Pressed' if pressed else 'Released'} at ({x}, {y}) with {button}")

def capture_screenshot():
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = os.path.join(SCREENSHOT_DIR, f'screenshot_{timestamp}.png')
        ImageGrab.grab().save(screenshot_path)
        print(f"Screenshot captured: {screenshot_path}")
        return screenshot_path
    except Exception as e:
        print(f"Failed to capture screenshot: {e}")
        return None

def save_activity(screenshot_path):
    if screenshot_path is not None:
        relative_path = os.path.relpath(screenshot_path, BASE_DIR).replace('\\', '/')
        if relative_path.startswith('static/'):
            relative_path = relative_path[len('static/'):]
        log = ActivityLog(
            screenshot_path=relative_path,
            keyboard_activity_count=keyboard_activity_count,
            mouse_activity_count=mouse_activity_count
        )
        session.add(log)
        session.commit()
        print(f"Activity saved: {log}")

def main():
    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_press)

    mouse_listener.start()
    keyboard_listener.start()

    print("Listeners started. Monitoring activity...")

    try:
        while True:
            time.sleep(180)  # Задержка в 3 минуты
            screenshot_path = capture_screenshot()
            save_activity(screenshot_path)
            global keyboard_activity_count, mouse_activity_count
            keyboard_activity_count = 0
            mouse_activity_count = 0
    except KeyboardInterrupt:
        mouse_listener.stop()
        keyboard_listener.stop()
        print("Monitoring stopped.")

if __name__ == '__main__':
    main()
