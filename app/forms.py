from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class PlaylistSearchForm(FlaskForm):
    uri = StringField('URI', validators=[DataRequired()])
    submit = SubmitField('Go !')
