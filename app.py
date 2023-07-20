from flask import Flask, render_template
from route import routes_page

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'assignment2-secret'

# Register routes from seperate route file
app.register_blueprint(routes_page)


if __name__ == '__main__':
    app.run(debug=True)