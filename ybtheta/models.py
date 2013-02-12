from datetime import date, datetime

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr

from ybtheta import db


class Brother(db.Model):
    __tablename__ = 'brothers'

    # Biographical info
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    full_name = db.Column(db.String(180))
    nickname = db.Column(db.String(100))
    birthday = db.Column(db.Date)
    picture = db.Column(db.String(200))
    # Theta Tau info
    roll_number = db.Column(db.Integer)
    page_number = db.Column(db.Integer)
    chapter = db.Column(db.String(100), nullable=False, default="Upsilon Beta")
    initiation = db.Column(db.Date)
    pledge_class = db.Column(db.String(100))
    big_id = db.Column(db.Integer, db.ForeignKey('brothers.id'), nullable=True)
    big_brother = db.relationship('Brother', backref='little_brothers',
            remote_side='Brother.id')
    current_positions = db.relationship('Position', back_populates='brother',
            primaryjoin='(Brother.id == Position.brother_id) & '\
            '(Position.current == True)')
    past_positions = db.relationship('Position', back_populates='brother',
            primaryjoin='(Brother.id == Position.brother_id) & '\
            '(Position.current == False)')
    status = db.Column(db.Enum('Alumni', 'Student', 'Co-Op', 'Inactive',
            'Pledge', name='brother_status'), nullable=False,
            default='Student')
    # Academic info
    graduation_date = db.Column(db.Date)
    major = db.Column(db.String(80))
    # Contact info
    emails = db.relationship('EmailAddress', backref='brother')
    phone_numbers = db.relationship('PhoneNumber', backref='brother')
    addresses = db.relationship('MailingAddress', backref='brother')
    # Misc stuff
    quotes = db.Column(db.Text())
    revision_timestamp = db.Column(db.DateTime(timezone=True), nullable=False,
            default=datetime.utcnow())


    def __repr__(self):
        return "<{}, {} #{} ({})>".format(self.name, self.chapter,
                self.roll_number, self.status)


class Position(db.Model):
    __tablename__ = 'positions'

    POSITIONS = {u'Corresponding Secretary': 'R',
             u'Inner Guard': 'T',
             u'Outer Guard': 'U',
             u'Scribe': 'V',
             u'Marshal': 'W',
             u'Regent': 'X',
             u'Vice Regent': 'Y',
             u'Treasurer': 'Z',
             u'Pledge Master': '',
             u'Pledge Instructor': ''
         }

    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Enum(*POSITIONS.keys(), name='position'),
            nullable=False)
    date = db.Column(db.Date)
    current = db.Column(db.Boolean, nullable=False, default=False)
    brother_id = db.Column(db.Integer, db.ForeignKey('brothers.id'))
    brother = db.relationship('Brother', single_parent=True)


    def __repr__(self):
        return "<{} - {}{}>".format(self.position, self.date, "!" if
                self.current else "")

class ContactInfoMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(60))

    @declared_attr
    def brother_id(cls):
        return db.Column(db.Integer, db.ForeignKey('brothers.id'))


class EmailAddress(ContactInfoMixin, db.Model):
    __tablename__ = 'emails'
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<{} ({})>".format(self.email, self.description)


class PhoneNumber(ContactInfoMixin, db.Model):
    __tablename__ = 'phonenumbers'
    phone_number = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return "<{} ({})>".format(self.phone_number, self.description)


class MailingAddress(ContactInfoMixin, db.Model):
    __tablename__ = 'addresses'
    address = db.Column(db.Text)

    def __repr__(self):
        return "<{} ({})>".format(self.address, self.description)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    real_name = db.Column(db.String(100))
    screen_name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, real_name, screen_name, email):
        self.real_name = real_name
        self.screen_name = screen_name
        self.email = email

    def __repr__(self):
        return "<User {}>".format(self.username)


class OpenID(db.Model):
    __tablename__ = 'openids'

    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(250), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('openids',
        lazy='dynamic'))

    def __init__(self, openid, user):
        self.openid = openid
        self.user = user

