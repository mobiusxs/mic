from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class AdminForm(FlaskForm):
    character_id = StringField('character_id', validators=[DataRequired()])
