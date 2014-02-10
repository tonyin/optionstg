# -*- coding: utf-8 -*-

from main import app
from flask import render_template, flash, redirect, url_for
import auth
from model import Section

# ########
# Routing
# ########

@app.route('/lesson/<int:lesson_id>/', methods=['GET'])
@auth.login_required
def lesson(lesson_id):
    user_db = auth.current_user_db()
    section_dbs = Section.query(Section.lesson == lesson_id)
    return render_template(
        'lesson.html',
        html_class='lesson',
        sections=section_dbs,
        title='Lesson ' + str(lesson_id),
        lesson_id=lesson_id,
        progress=user_db.progress,
    )
