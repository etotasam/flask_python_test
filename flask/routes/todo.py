from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Todo
from scraping_yahoo import test

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@todo_bp.route('/add', methods=['POST'])
def add_todo():
    content = request.form.get('content')
    new_todo = Todo(content=content)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('todo.index'))

@todo_bp.route('/complete/<int:todo_id>')
def complete(todo_id):
    todo = Todo.query.get(todo_id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for('todo.index'))

@todo_bp.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo.index'))


@todo_bp.route('/test', methods=['GET'])
def get_data():
    img_src_list = test()
    return render_template('saerce.html', data=img_src_list)