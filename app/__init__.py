# app/__init__.py
from flask import Flask, render_template
from flask import Flask
from flask_mysqldb import MySQL
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
import mysql.connector


mysql = MySQL()

def test_db_connection(app):
    try:
        # Establish a connection to the database
        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        
        if connection.is_connected():
            print("Database connection successful!")
            return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        if connection.is_connected():
            connection.close()

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        MYSQL_NAME=DB_NAME,
        MYSQL_PASSWORD=DB_PASSWORD,
        MYSQL_DB=DB_NAME,
        MYSQL_HOST=DB_HOST,
        MYSQL_USER=DB_USER
    )

    mysql.init_app(app)

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
