# coding=utf-8
from flask import render_template, request, redirect, url_for, flash

from ybtheta import app, db
from ybtheta.models import (Brother, Position, EmailAddress, PhoneNumber,
    MailingAddress)
from ybtheta.forms import BrotherForm


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
    return render_template('brother_detail.html', brother=brother,
            form=BrotherForm(obj=brother))


@app.route('/brothers/id/<int:id_num>')
def brother_detail_id(id_num):
    brother = Brother.query.get_or_404(id_num)
    if brother.roll_number is not None:
        return redirect(url_for('brother_detail',
            roll_num=brother.roll_number))
    return render_template('brother_detail.html', brother=brother,
            form=BrotherForm(obj=brother))


@app.route('/brothers/<int:roll_num>/edit', methods=['GET', 'POST'],
        defaults={'id_num': None})
@app.route('/brothers/id/<int:id_num>/edit', methods=['GET', 'POST'],
        defaults={'roll_num': None})
def edit_brother(roll_num, id_num):
    if id_num:
        brother = Brother.query.get(id_num)
    else:
        brother = Brother.query.filter_by(roll_number=roll_num).order_by(
                Brother.page_number).first()
    form = BrotherForm(request.form, brother)
    if form.validate_on_submit():
        flash(u"Brother updated", 'success')
        for field in form:
            print "{name}: {value}".format(name=field.name, value=field.data)
        form.populate_obj(brother)
        db.session.commit()
        if id_num:
            return redirect(url_for('brother_detail_id', id_num=id_num))
        else:
            return redirect(url_for('brother_details', roll_num=roll_num))
    return render_template('brother_detail.html', brother=brother, form=form,
            start_edit=True)

