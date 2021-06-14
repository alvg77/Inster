from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SearchForm(FlaskForm):
    search = StringField('Search')
    submit = SubmitField('Search')