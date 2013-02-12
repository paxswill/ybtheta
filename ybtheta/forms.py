from flask.ext.wtf import (Form, TextField, TextAreaField, DateField,
        HiddenField, Required, Optional)
from flask.ext.wtf.html5 import EmailField, TelField, IntegerField


class BrotherForm(Form):
    id = HiddenField()
    name = TextField('Name', validators=[Required()])
    full_name = TextField('Full Name')
    nickname = TextField('Nickname')
    birthday = DateField('Birthday', validators=[Optional()])
    # picture
    roll_number = IntegerField('Roll Number', validators=[Optional()])
    page_number = IntegerField('Page Number', validators=[Optional()])
    chapter = TextField('Chapter', validators=[Required()])
    initiation = DateField('Initiation Date', validators=[Optional()])
    pledge_class = TextField('Pledge Class')
    # big_brother
    # current_positions
    # past_positions
    graduation_date = DateField('Graduation Date', validators=[Optional()])
    major = TextField('Major')
    # emails
    # phone_numbers
    # addresses
    quotes = TextAreaField('Quotes')


class LoginForm(Form):
    openid = TextField('OpenID URL', validators=[Required()])


class CreateAccountForm(Form):
    real_name = TextField('Real Name', validators=[Required()])
    screen_name = TextField('Screen Name', validators=[Required()])
    email = TextField('Email', validators=[Required()])

