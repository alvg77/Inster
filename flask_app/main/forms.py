from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[Length(min=3)])
    submit = SubmitField('Search')