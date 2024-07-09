from flask import request, redirect, url_for, render_template, jsonify
from views.decorators import login_required
from models.task import Task
from models.engine import Session
from views import app_views

@app_views.route('/tasks', methods=['GET', 'POST'])
# @login_required
def manage_tasks():
    if request.method == 'POST':
        data = request.json
        
        if not all(key in data for key in ('description', 'status', 'event_id')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        new_task = Task(
            description=data['description'],
            status=data['status'],
            event_id=data['event_id'],
            #due_date=data['due_date']
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

    elif request.method == 'GET':
        session = Session()
        tasks = session.query(Task).all()
        session.close()
        
        return render_template('task.html', tasks=tasks)

@app_views.route('/tasks/<int:task_id>', methods=['PUT'])
# @login_required
def update_task(task_id):
    session = Session()
    
    task = session.query(Task).filter(Task.task_id == task_id).first()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.json
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    #task.due_date = data.get('due_date', task.due_date)
    task.event_id = data.get('event_id', task.event_id)
    #task.task_id = data.get('task_id', task.task_id)

    session.commit()
    session.close()
    
    return jsonify({'message': 'Task updated successfully'}), 200
