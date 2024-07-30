from flask import Flask, render_template
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from datetime import *

app = Flask(__name__)

# Настройка базы данных
DATABASE_URL = r'sqlite:///C:\Users\New\PycharmProjects\tracker\activity_tracker.db'
engine = sa.create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Определение модели для чтения данных
class ActivityLog(Base):
    __tablename__ = 'activity_log'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    timestamp = sa.Column(sa.DateTime, default=datetime.utcnow)
    screenshot_path = sa.Column(sa.String)
    keyboard_activity = sa.Column(sa.String)
    mouse_activity = sa.Column(sa.String)

@app.route('/')
def index():
    logs = session.query(ActivityLog).order_by(ActivityLog.timestamp.desc()).all()
    return render_template('index.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True)
