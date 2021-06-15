from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed


class ActionForm(FlaskForm):
    submit = SubmitField('Action')
    
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=25)])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])    
    content = TextAreaField('Content', validators=[DataRequired(), Length(max=200)])
    remove_img = SubmitField('Remove')
    submit = SubmitField('Post')

class CommentsForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Post')