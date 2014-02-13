# -*- coding: utf-8 -*-

from main import app
from flask import render_template, flash, redirect, url_for
import auth
from model import Section

# ########
# Routing
# ########

@app.route('/lesson/', defaults={'lesson_id': 0, 'section_id': 1})
@app.route('/lesson/<int:lesson_id>/', defaults={'lesson_id': 0, 'section_id': 1}, methods=['GET'])
@app.route('/lesson/<int:lesson_id>/<int:section_id>/', methods=['GET'])
@auth.login_required
def lesson(lesson_id, section_id):
    user_db = auth.current_user_db()
    if user_db.progress < lesson_id:
        return redirect(url_for('lesson', lesson_id=user_db.progress, section_id=1))
    section_dbs = Section.query(Section.lesson == lesson_id).order(Section.number)
    return render_template(
        'lesson.html',
        html_class='lesson',
        sections=section_dbs,
        title='Lesson ' + str(lesson_id),
        lesson_id=lesson_id,
        section_id=section_id,
        progress=user_db.progress,
    )
