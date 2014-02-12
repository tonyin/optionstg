# -*- coding: utf-8 -*-

from main import app
from flask.ext import wtf
from flask import render_template, flash, redirect, url_for
import auth
from model import Section

# ########
# Globals
# ########


# ######
# Forms
# ######
class SectionForm(wtf.Form):
    title = wtf.StringField('Title', [wtf.validators.required()])
    content = wtf.TextAreaField('Content', [wtf.validators.optional()])
    lesson = wtf.IntegerField('Lesson', [wtf.validators.NumberRange(min=0, max=5)])
    number = wtf.IntegerField('Number', [wtf.validators.NumberRange(min=1, max=9)])

# ########
# Routing
# ########

@app.route('/section/view/')
@auth.admin_required
def section_view():
    section_dbs = Section.query()
    return render_template(
        'section_view.html',
        html_class='section-view',
        title='Sections',
        sections=section_dbs
        )

@app.route('/section/create/', methods=['GET', 'POST'])
@auth.admin_required
def section_create():
    form = SectionForm()
    if form.validate_on_submit():
        section_db = Section(
            title = form.title.data,
            content = form.content.data,
            lesson = form.lesson.data,
            number = form.number.data,
        )
        try:
            section_db.put()
            flash(u'Section id %s successfully saved.' % section_db.key.id(), 'success')
            return redirect(url_for('section_view'))
        except:
            flash(u'Something went wrong.', 'info')
            return redirect(url_for('section_update'))
    return render_template(
        'section_update.html',
        html_class='section-create',
        title='Create Section',
        form=form)

@app.route('/section/<int:section_id>/delete/', methods=['GET', 'POST'])
@auth.admin_required
def section_delete(section_id):
    section_db = Section.get_by_id(section_id)
    try:
        section_db.key.delete()
        flash(u'Section id %s successfully deleted.' % section_id, 'success')
        return redirect(url_for('section_view'))
    except:
        flash(u'Something went wrong.', 'info')
        return redirect(url_for('section_view'))

@app.route('/section/<int:section_id>/update/', methods=['GET', 'POST'])
@auth.admin_required
def section_update(section_id):
    section_db = Section.get_by_id(section_id)
    form = SectionForm(obj=section_db)
    if form.validate_on_submit():
        form.populate_obj(section_db)
        try:
            section_db.put()
            flash(u'Section id %s successfully saved.' % section_db.key.id(), 'success')
            return redirect(url_for('section_view'))
        except:
            flash(u'Something went wrong.', 'info')
            return redirect(url_for('section_view'))
    return render_template(
        'section_update.html',
        html_class='section-update',
        title='Edit Section',
        form=form,
        section_db=section_db
    )
