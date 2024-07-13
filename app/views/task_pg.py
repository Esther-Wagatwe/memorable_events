from flask import request, redirect, url_for, render_template, jsonify
from flask_login import login_required
from models.task import Task
from models.engine import Session
from views import app_views
import datetime


@app_views.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    session = Session()
    tasks = session.query(Task).all()
    session.close()
    # return jsonify([task.serialize() for task in tasks])
    return render_template('task.html', tasks=tasks)

@app_views.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    session = Session()
    task = session.query(Task).get(task_id)
    session.close()
    if task:
        return jsonify(task.serialize())
    else:
        return jsonify({'error': 'Task not found'}), 404
    

@app_views.route('/tasks', methods=['POST'])
def create_task():
        data = request.json
        
        if not all(key in data for key in ('description', 'status', 'event_id')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        new_task = Task(
            description=data['description'],
            status=data.get('status', 'pending'),
            event_id=data['event_id'],
            due_date=datetime.datetime.strptime(data['due_date'], '%Y-%m-%d').date()
        )
        
        session = Session()
        try:
            session.add(new_task)
            session.commit()
            return jsonify({'message': 'Task created successfully'}), 201
        except Exception as e:
            session.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            session.close()


@app_views.route('/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    session = Session()
    task = session.query(Task).get(task_id)
    
    if not task:
        session.close()
        return jsonify({'error': 'Task not found'}), 404
    
    try:
        data = request.json
        
        if 'description' in data:
            task.description = data['description']
        
        if 'status' in data:
            task.status = data['status']
        
        if 'event_id' in data:
            task.event_id = data['event_id']
        
        if 'due_date' in data:
            task.due_date = datetime.datetime.strptime(data['due_date'], '%Y-%m-%d').date()
        
        session.commit()
        session.close()
        return jsonify({'message': 'Task updated successfully'})
    
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@app_views.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    session = Session()
    task = session.query(Task).get(task_id)
    if task:
        session.delete(task)
        session.commit()
        session.close()
        return jsonify({'message': 'Task deleted successfully'})
    else:
        session.close()
        return jsonify({'error': 'Task not found'}), 404