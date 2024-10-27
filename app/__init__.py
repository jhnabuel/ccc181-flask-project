# app/__init__.py
from flask import Flask, render_template
from flask import Flask
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
import mysql.connector
import os
from config import configure_cloudinary

mysql = MySQL()
csrf = CSRFProtect()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)
    
    # Load configuration from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MYSQL_USER'] = os.getenv('DB_USER')
    app.config['MYSQL_USERNAME'] = os.getenv('DB_USERNAME')
    app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('DB_NAME')
    app.config['MYSQL_HOST'] = os.getenv('DB_HOST')

    csrf.init_app(app)
    mysql.init_app(app)
    configure_cloudinary(app)
    

    # Routing the master template (index.html) directly
    @app.route('/')
    def index():
        return render_template('index.html')
    

    # Import and register the students blueprint
    from .students import students as students_blueprint
    app.register_blueprint(students_blueprint)

    from .courses import courses as courses_blueprint
    app.register_blueprint(courses_blueprint)

    from .colleges import colleges as colleges_blueprint
    app.register_blueprint(colleges_blueprint)

    return app

