# -*- coding: utf-8 -*-

from main import app
from flask.ext import wtf
from flask import render_template, flash, redirect, url_for
import auth
from model import Lesson, Section, Piece

# ######
# Forms
# ######
class LessonForm(wtf.Form):
    title = wtf.StringField('Title', [wtf.validators.required()])
    number = wtf.IntegerField('Number', [wtf.validators.optional(), wtf.validators.NumberRange(min=0, max=5)])

# ########
# Routing
# ########

@app.route('/lesson/', defaults={'lesson_id': 0, 'section_id': 1}, methods=['GET'])
@app.route('/lesson/<int:lesson_id>/', defaults={'lesson_id': 0, 'section_id': 1}, methods=['GET'])
@app.route('/lesson/<int:lesson_id>/<int:section_id>/', methods=['GET'])
@auth.login_required
def lesson(lesson_id, section_id):
    user_db = auth.current_user_db()
    if user_db.progress < lesson_id:
        return redirect(url_for('lesson', lesson_id=user_db.progress, section_id=1))
    if not user_db.registered:
        return redirect(url_for('welcome'))
    #if form.validate_on_submit():
        
    lesson_db = Lesson.query(Lesson.number == lesson_id)
    section_dbs = Section.query(Section.lesson == lesson_id).order(Section.number)
    piece_dbs = Piece.query(Piece.lesson == lesson_id, Piece.section == section_id).order(Piece.number)
    graph_string = 'graphs/graph_' + str(lesson_id) + '_' + str(section_id)
    return render_template(
        'lesson.html',
        html_class='lesson',
        lesson=lesson_db,
        sections=section_dbs,
        pieces=piece_dbs,
        graph=graph_string + '.html',
        graph_head=graph_string + '_head.html',
        lesson_id=lesson_id,
        section_id=section_id,
        progress=user_db.progress
    )

# ################
# Routing - Admin
# ################

@app.route('/lesson/view/')
@auth.admin_required
def lesson_view():
    lesson_dbs = Lesson.query().order(Lesson.number)
    return render_template(
        'lesson_view.html',
        html_class='lesson-view',
        title='Lessons',
        lessons=lesson_dbs,
    )

@app.route('/lesson/create/', methods=['GET', 'POST'])
@auth.admin_required
def lesson_create():
    form = LessonForm()
    if form.validate_on_submit():
        lesson_db = Lesson(
            title = form.title.data,
            number = form.number.data,
        )
        try:
            lesson_db.put()
            flash(u'Lesson id %s successfully saved.' % lesson_db.key.id(), 'success')
            return redirect(url_for('lesson_view'))
        except:
            flash(u'Something went wrong.', 'info')
            return redirect(url_for('lesson_update'))
    return render_template(
        'lesson_update.html',
        html_class='lesson-create',
        title='Create Lesson',
        form=form)

@app.route('/lesson/<int:lesson_id>/delete/', methods=['GET', 'POST'])
@auth.admin_required
def lesson_delete(lesson_id):
    lesson_db = Lesson.get_by_id(lesson_id)
    try:
        lesson_db.key.delete()
        flash(u'Lesson id %s successfully deleted.' % lesson_id, 'success')
        return redirect(url_for('lesson_view'))
    except:
        flash(u'Something went wrong.', 'info')
        return redirect(url_for('lesson_view'))

@app.route('/lesson/<int:lesson_id>/update/', methods=['GET', 'POST'])
@auth.admin_required
def lesson_update(lesson_id):
    lesson_db = Lesson.get_by_id(lesson_id)
    form = LessonForm(obj=lesson_db)
    if form.validate_on_submit():
        form.populate_obj(lesson_db)
        try:
            lesson_db.put()
            flash(u'Lesson id %s successfully saved.' % lesson_db.key.id(), 'success')
            return redirect(url_for('lesson_view'))
        except:
            flash(u'Something went wrong.', 'info')
            return redirect(url_for('lesson_view'))
    return render_template(
        'lesson_update.html',
        html_class='lesson-update',
        title='Edit Lesson',
        form=form,
        lesson_db=lesson_db
    )
