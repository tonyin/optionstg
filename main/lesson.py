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
    if lesson_id == 0:
        section_dbs = Section.query(Section.lesson == 0)
        title = "Lesson 0"
    else:
        title = "Lesson Something"
    return render_template(
        'lesson.html',
        html_class='lesson',
        title=title,
        sections=section_dbs
        )
