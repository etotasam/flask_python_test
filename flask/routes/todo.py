from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for
from models import Todo, db
import logging
import datetime
import pytz

todo_bp = Blueprint('todo', __name__)

jst = pytz.timezone('Asia/Tokyo')
current_date = datetime.datetime.now(jst).strftime('%Y%m%d')

# logを保存するディレクトリが存在しない時は作成
directory_name = 'log'
log_directory = Path(directory_name)
if not log_directory.exists():
    log_directory.mkdir()

log_handler = logging.FileHandler(f'{directory_name}/{current_date}.log')
log_handler.setLevel(logging.INFO)
log_format = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
log_handler.setFormatter(log_format)
logger = logging.getLogger('my_logger')
logger.addHandler(log_handler)


@todo_bp.route('/')
def index():
    todos = Todo.query.all()
    logging.debug('いんでっくす')
    logger.info('test_いんふぉ')
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