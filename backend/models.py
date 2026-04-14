from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# Инициализируем объект БД (привязка к приложению будет в app.py)
db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    # Используем современный способ получения UTC времени
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        """Вспомогательный метод для сериализации объекта в JSON"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<Task {self.title}>'
