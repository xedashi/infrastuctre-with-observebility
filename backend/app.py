import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from dotenv import load_dotenv

# Импортируем объект db и модель из нашего файла models.py
from models import db, Task

# Загружаем переменные окружения из .env
load_dotenv()

# Создаем приложение (шаблоны больше не нужны!)
app = Flask(__name__)

# Конфигурация приложения
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_dev_key')

# Инициализация расширений
db.init_app(app)
migrate = Migrate(app, db)


# --- REST API Эндпоинты ---
# Все роуты начинаются с /api/ для корректной маршрутизации через Nginx

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Получение списка всех задач."""
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    # Используем наш метод to_dict() для превращения объектов БД в словари
    return jsonify([task.to_dict() for task in tasks]), 200


@app.route('/api/tasks', methods=['POST'])
def add_task():
    """Создание новой задачи."""
    data = request.get_json() # Получаем данные из JSON-тела запроса
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    title = data.get('title')
    description = data.get('description', '')

    if title and title.strip():
        new_task = Task(title=title.strip(), description=description.strip())
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task created', 'task': new_task.to_dict()}), 201

    return jsonify({'error': 'Title is required'}), 400


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Удаление задачи по её ID."""
    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted successfully'}), 200


if __name__ == '__main__':
    # В Docker мы слушаем все интерфейсы (0.0.0.0), иначе снаружи не достучаться
    app.run(host='0.0.0.0', port=5000, debug=True)
