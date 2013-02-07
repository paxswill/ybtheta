# coding=utf-8
from flask import render_template
from ybtheta import app, db


@app.route('/brothers')
def brothers():
    return render_template('placeholder.html', name='brothers')


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
    roll_number = db.Column(db.Integer, nullable=False)
    page_number = db.Column(db.Integer, nullable=False, unique=True)
    chapter = db.Column(db.String(100), nullable=False)
    initiation = db.Column(db.Date)
    pledge_class = db.Column(db.String(100))
    big_id = db.Column(db.Integer, db.ForeignKey('brothers.id'))
    big_brother = db.relationship('Brother', backref='little_brothers')
    current_positions = db.relationship('Position', backref='brother')
    past_positions = db.relationship('Position', backref='brother')
    status = db.Column(db.Enum('Alumni', 'Student', 'Co-op', 'Inactive',
        'Pledge', name='brother_status'), nullable=False, default='Student')
    # Academic info
    graduation_date = db.Column(db.Date)
    major = db.Column(db.String(80))
    # Contact info
    emails = db.relationship('EmailAddress', backref='brother')
    phone_numbers = db.relationship('PhoneNumber', backref='brother')
    addresses = db.relationship('MailingAddress', backref='brother')


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Enum(*POSITIONS.keys(), name='position'),
            nullable=False)
    brother_id = db.Column(db.Integer, db.ForeignKey('brothers.id'))


class EmailAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brother_id = db.Column(db.Integer, db.ForeignKey('brothers.id'))
    description = db.Column(db.String(60))
    email = db.Column(db.String(100), nullable=False)


class PhoneNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brother_id = db.Column(db.Integer, db.ForeignKey('brothers.id'))
    description = db.Column(db.String(60))
    phone_number = db.Column(db.String(30), nullable=False)


STATES = {
        u'Washington': 'WA',
        u'Oregon': 'OR',
        u'California': 'CA',
        u'Nevada': 'NV',
        u'Hawaii': 'HI',
        u'Alaska': 'AK',
        u'Idaho': 'ID',
        u'Montana': 'MT',
        u'Wyoming': 'WY',
        u'Colorado': 'CO',
        u'New Mexico': 'NM',
        u'Arizona': 'AZ',
        u'Utah': 'UT',
        u'North Dakota': 'ND',
        u'South Dakota': 'SD',
        u'Nebraska': 'NE',
        u'Kansas': 'KS',
        u'Oklahoma': 'OK',
        u'Texas': 'TX',
        u'Arkansas': 'AR',
        u'Louisiana': 'LA',
        u'Missouri': 'MO',
        u'Michigan': 'MI',
        u'Minnesota': 'MN',
        u'Wisconsin': 'WI',
        u'Iowa': 'IA',
        u'Indiana': 'IN',
        u'Ohio': 'OH',
        u'Illinois': 'IL',
        u'Kentucky': 'KY',
        u'Tennessee': 'TN',
        u'Alabama': 'AL',
        u'Mississippi': 'MS',
        u'Georgia': 'GA',
        u'Florida': 'FL',
        u'South Carolina': 'SC',
        u'North Carolina': 'NC',
        u'Virginia': 'VA',
        u'West Virginia': 'WV',
        u'Pennsylvania': 'PA',
        u'New Jersey': 'NJ',
        u'Maryland': 'MD',
        u'New York': 'NY',
        u'Vermont' : 'VT',
        u'Connecticut': 'CT',
        u'Massachusetts': 'MA',
        u'New Hampshire': 'NH',
        u'Maine': 'ME',
        u'Rhode Island': 'RI',
        # Got this far and forgot Delware... so close
        u'Delaware': 'DE',
        u'District of Columbia': 'DC',
        u'Puerto Rico': 'PR',
        u'Virgin Islands': 'VI',
        u'Guam': 'GU',
        u'Northern Mariana Islands': 'MP',
        u'American Samoa': 'AS',
        u'Micronesia': 'FM',
        u'Marshall Islands': 'MH',
        u'Palau': 'PW',
        u'U.S. Military – Americas': 'AA',
        u'U.S. Military – Europe': 'AE',
        u'U.S. Military – Pacific': 'AP',
        u'British Columbia': 'BC',
        u'Manitoba': 'MB',
        u'New Brunswick': 'NB',
        u'Quebec': 'QC',
        u'Northern Territories': 'NT',
        u'Nunavut': 'NU',
        u'Alberta': 'AB',
        u'Newfoundland and Labrador': 'NL',
        u'Nova Scotia': 'NS',
        u'Ontario': 'ON',
        u'Prince Edward Island': 'PE',
        u'Saskatchewan': 'SK',
        u'Yukon': 'YT'
    }


class MailingAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brother_id = db.Column(db.Integer, db.ForeignKey('brothers.id'))
    line_1 = db.Column(db.String(100))
    line_2 = db.Column(db.String(100))
    city = db.Column(db.String(80))
    postal_code = db.Column(db.String(20))
    state = db.Column(db.Enum(*STATES.values()))
    description = db.Column(db.String(60))

