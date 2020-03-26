from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField, TextAreaField, StringField, SelectMultipleField, SubmitField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired


class PostForm(FlaskForm):
    title = StringField('Назва', validators=[DataRequired()])
    description = StringField('Опис', validators=[DataRequired])
    body = PageDownField('Зміст', validators=[DataRequired()])
    image = FileField('Додати зображення', validators=[DataRequired()])
    tags = SelectMultipleField(u'Обрати наявні теги', coerce=int, validators=[DataRequired()])

    submit_post = SubmitField('Створити')


class TagForm(FlaskForm):
    add_tag = StringField('Додати тег', validators=[DataRequired()])
    submit_tag = SubmitField('Додати')

class ImageForm(FlaskForm):
    add_img = FileField('Додати зображення', validators=[DataRequired()])
    submit_img = SubmitField('Додати')