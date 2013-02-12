from flask.ext.wtf import (Form, BooleanField, DateField, FieldList,
        FormField, HiddenField, RadioField, SelectField, TextField,
        TextAreaField, Email, Optional, Required)
from flask.ext.wtf.html5 import EmailField, TelField, IntegerField
from wtforms import Form as WTForm

from ybtheta.models import Position


class PositionForm(WTForm):
    id = HiddenField()
    position = SelectField('Position', choices=
            [(val, val) for val in Position.POSITIONS.keys()])
    date = DateField('Start Date', validators=[Optional()])
    current = BooleanField('Current', default=False, validators=[Required()])


class BrotherContactInfo(WTForm):
    id = HiddenField()
    description = TextField('Description')


class BrotherEmail(BrotherContactInfo):
    email = EmailField('Email address', validators=[Email()])


class BrotherPhoneNumber(BrotherContactInfo):
    phone_number = TelField('Telephone number')


class BrotherAddress(BrotherContactInfo):
    address = TextAreaField('Mailing address')


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
    positions = FieldList(FormField(PositionForm))
    status = SelectField('Status', choices=[(val, val) for val in ('Alumni',
        'Student', 'Co-Op', 'Inactive', 'Pledge')])
    graduation_date = DateField('Graduation Date', validators=[Optional()])
    major = TextField('Major')
    emails = FieldList(FormField(BrotherEmail))
    phone_number = FieldList(FormField(BrotherPhoneNumber))
    addresses = FieldList(FormField(BrotherAddress))
    quotes = TextAreaField('Quotes')


class LoginForm(Form):
    openid = TextField('OpenID URL', validators=[Required()])


class CreateAccountForm(Form):
    real_name = TextField('Real Name', validators=[Required()])
    screen_name = TextField('Screen Name', validators=[Required()])
    email = TextField('Email', validators=[Required()])

