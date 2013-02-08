#!/usr/bin/env python
from time import mktime, strptime
from datetime import date, datetime
from calendar import timegm

import MySQLdb as sql

from ybtheta import db
import ybtheta.brothers as bro


def ts2dt(timestamp):
    try:
        time_struct = strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        time_struct = strptime(timestamp, '%Y-%m-00T%H:%M:%S')
    epoch_time = timegm(time_struct)
    return datetime.fromtimestamp(epoch_time)


# Create the destination db
db.create_all()

# Set up the source connection
conn = sql.connect(host='127.0.0.1', user='root', passwd='root', port=3306,
        db='thetheta_thetatauodu', use_unicode=True)

crs = conn.cursor()

# The two content types we care about are brother and story.
crs.execute("""SELECT yb_node.title,
yb_content_type_brother.field_full_name_value,
yb_node.nid,
yb_content_type_brother.field_roll_num_value,
yb_content_type_brother.field_chapter_value,
yb_content_type_brother.field_inititation_value,
yb_content_type_brother.field_big_nid,
yb_content_type_brother.field_grad_date_value,
yb_content_type_brother.field_major_value,
yb_content_type_brother.field_staus_value,
yb_content_type_brother.field_page_num_value,
yb_content_type_brother.field_mail_addr_value,
yb_content_type_brother.field_nickname_value,
yb_content_type_brother.field_pledge_class_value,
yb_content_type_brother.field_birthday_value,
yb_content_type_brother.field_brother_quotes_value,
yb_node.changed
FROM yb_node INNER JOIN yb_content_type_brother
ON yb_node.nid = yb_content_type_brother.nid;""")

brother_lookup = {}

big_relations = {}

# Fill in most of the brother info
for brother in crs.fetchall():
    new_bro = bro.Brother(
            name=brother[0],
            full_name=brother[1],
            # Skipping 2, nid
            roll_number=brother[3],
            chapter=brother[4],
            # Skipping 6, big_nid
            major=brother[8],
            status=brother[9],
            page_number=brother[10],
            # skipping 11, mailing address
            nickname=brother[12],
            pledge_class=brother[13],
            quotes=brother[15],
            revision_timestamp=datetime.utcfromtimestamp(brother[16]))
    address = bro.MailingAddress(address=brother[11])
    address.brother = new_bro
    if brother[5]:
        new_bro.initiation=ts2dt(brother[5]).date()
    if brother[7]:
        new_bro.graduation_date=ts2dt(brother[7]).date()
    if brother[14]:
        new_bro.birthday=ts2dt(brother[14]).date()
    # Save the new objects
    brother_lookup[brother[2]] = new_bro
    # Save the Big brother for once we have all brother imported
    if brother[6]:
        big_relations[brother[2]] = brother[6]
    db.session.add(new_bro)
db.session.commit()

# Link the littles to bigs
for little_id, big_id in big_relations.items():
    brother_lookup[little_id].big_brother = brother_lookup[big_id]
db.session.commit()

# Transfer the phone numbers
crs.execute("""SELECT nid, field_phone_value FROM yb_content_field_phone WHERE
        field_phone_value IS NOT NULL;""")
for phone in crs.fetchall():
    new_number = bro.PhoneNumber(phone_number=phone[1])
    new_number.brother = brother_lookup[phone[0]]
db.session.commit()

# Transfer over email addresses
crs.execute("""SELECT nid, field_email_addr_value FROM
yb_content_field_email_addr WHERE
field_email_addr_value IS NOT NULL;""")
for email in crs.fetchall():
    new_email = bro.EmailAddress(email=email[1])
    new_email.brother = brother_lookup[email[0]]
db.session.commit()

# And now the positions
crs.execute("""SELECT nid, field_current_position_value
FROM yb_content_field_current_position
WHERE field_current_position_value IS NOT NULL;""")
for position in crs.fetchall():
    new_pos = bro.Position(position=position[1], current=True)
    brother_lookup[position[0]].current_positions.append(new_pos)
crs.execute("""SELECT nid, field_positions_value
FROM yb_content_field_positions
WHERE field_positions_value IS NOT NULL;""")
for position in crs.fetchall():
    new_pos = bro.Position(position=position[1])
    brother_lookup[position[0]].past_positions.append(new_pos)
db.session.commit()


conn.close()
