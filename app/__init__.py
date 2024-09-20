# app/__init__.py
from flask import Flask, render_template
def create_app():
    app = Flask(__name__)


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
