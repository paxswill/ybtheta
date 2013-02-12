# coding=utf-8
from datetime import date, datetime

from flask import render_template
from ybtheta import app, db


# Flask Views
@app.route('/brothers')
def student_members():
    ctx = {'brothers': Brother.query.filter_by(status='Student').\
                order_by(Brother.page_number).all()}
    pledges = Brother.query.filter_by(status='Pledge').order_by(Brother.name).\
            all()
    if len(pledges) > 0:
        ctx['pledges'] = pledges
    return render_template('brothers_thumbs.html', name='Students',
            top_name='brothers', **ctx)


@app.route('/brothers/all')
def all_brothers():
    print "Tracing..."
    brothers = Brother.query.filter(Brother.status != 'Pledge').order_by(
            Brother.page_number).all()
    return render_template('brothers_all.html', brothers=brothers,
            name='All Brothers', top_name='brothers')


@app.route('/brothers/alumni')
def alumni():
    alumni = Brother.query.filter(
            (Brother.status != 'Student') &
            (Brother.status != 'Pledge')).order_by(
                    Brother.page_number).all()
    return render_template('brothers_thumbs.html', brothers=alumni,
            name='Alumni', top_name='brothers')


@app.route('/brothers/<int:roll_num>', defaults={'ordinal': -1})
@app.route('/brothers/<int:roll_num>/<int:ordinal>')
def brother_detail(roll_num, ordinal):
    brother_query = Brother.query.filter_by(roll_number=roll_num)
    # Every brother /should/ have a unique page and roll number, but because
    # of transcription errors, source errors, and in some cases, laziness,
    # this is not always the case. By specifying an ordinal, we can stp through
    # Brothers with the same roll number, sorted by page_number.
    # -1 is used as a sentinel value, to not care which Brother to retrieve.
    if ordinal >= 0:
        brother_query = brother_query.order_by(Brother.page_number)
        brother_query = brother_query.offset(ordinal)
    # We only need one Brother
    brother_query = brother_query.limit(1)
    brother = brother_query.first_or_404()
    return render_template('brother_detail.html', brother=brother)


# SQLAlchemy models
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


class EmailAddress(db.Model):
    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True)
    brother_id = db.Column(db.Integer, db.ForeignKey('brothers.id'))
    description = db.Column(db.String(60))
    email = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return "<{} ({})>".format(self.email, self.description)


class PhoneNumber(db.Model):
    __tablename__ = 'phonenumbers'

    id = db.Column(db.Integer, primary_key=True)
    brother_id = db.Column(db.Integer, db.ForeignKey('brothers.id'))
    description = db.Column(db.String(60))
    phone_number = db.Column(db.String(30), nullable=False)


    def __repr__(self):
        return "<{} ({})>".format(self.phone_number, self.description)


class MailingAddress(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    brother_id = db.Column(db.Integer, db.ForeignKey('brothers.id'))
    address = db.Column(db.Text)
    description = db.Column(db.String(60))


    def __repr__(self):
        return "<{} ({})>".format(self.address, self.description)
