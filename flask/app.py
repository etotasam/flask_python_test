import os
from flask import Flask
import logging
from flask_migrate import Migrate
# ! module
from routes.todo import todo_bp
from routes.product import product_bp
from models import db

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
log_directory = "log"
log_dir_path = os.path.join(basedir, log_directory)
if not os.path.exists(log_dir_path):
    os.makedirs(log_dir_path)
print(f'テストファイル名:{log_dir_path}')
logging.basicConfig(filename=f'{log_directory}/app.log', level=logging.DEBUG)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "db/todo.db")}'

migrate = Migrate(app, db)
db.init_app(app)
# ! Blueprintを設定
app.register_blueprint(todo_bp)
app.register_blueprint(product_bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)