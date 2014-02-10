# -*- coding: utf-8 -*-

from main import app, welcome
from flask.ext import wtf
from flask import render_template, flash, redirect, url_for
import auth
import model
import util

# ########
# Globals
# ########
LESSONS = range(5)

# ######
# Forms
# ######
class SectionForm(wtf.Form):
    title = wtf.StringField('Title', [wtf.validators.required()])
    content = wtf.TextAreaField('Content', [wtf.validators.optional()])
    lesson = wtf.IntegerField('Lesson', [wtf.validators.AnyOf(LESSONS)])

# ########
# Routing
# ########
@app.route('/lesson/')
@auth.login_required
def lesson():
    return render_template('lesson.html', html_class='lesson')

@app.route('/section/view/')
@auth.admin_required
def section_view():
    section_dbs = model.Section.query()
    return render_template(
        'section_view.html',
        html_class='section-view',
        title='View Sections',
        sections=section_dbs
        )

@app.route('/section/create/', methods=['GET', 'POST'])
@auth.admin_required
def section_create():
    form = SectionForm()
    if form.validate_on_submit():
        section_db = model.Section(
            title = form.title.data,
            content = form.content.data,
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
    section_db = model.Section.get_by_id(section_id)
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
    section_db = model.Section.get_by_id(section_id)
    form = SectionForm()
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
        title=section_db.title,
        form=form,
        section_db=section_db
    )
