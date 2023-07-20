from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class AddForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle')
    author  = StringField('Author', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')
