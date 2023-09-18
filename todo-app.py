from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

# Create a Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def as_dict(self):
        return {'id': self.id, 'title': self.title, 'completed': self.completed}

# API routes
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all() # get al tasks
    tasks_dict = [task.as_dict() for task in tasks]
    return jsonify({'tasks': tasks_dict})

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(title=data['title'], completed=False)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully'})

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if task:
        data = request.get_json()
        task.title = data['title']
        task.completed = data['completed']
        db.session.commit()
        return jsonify({'message': 'Task updated successfully'})
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'})
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    # Create the database tables
    db.create_all()
    
    # Run the Flask app
    app.run(debug=True)
