import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from scraping_yahoo import test
import logging
from flask_migrate import Migrate
from routes.todo import todo_bp
from models import db

app = Flask(__name__)
logging.basicConfig(filename='app.log', level=logging.DEBUG)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "db/todo.db")}'

migrate = Migrate(app, db)
db.init_app(app)
app.register_blueprint(todo_bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)