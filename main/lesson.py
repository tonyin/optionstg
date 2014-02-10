# -*- coding: utf-8 -*-

from main import app
from flask import render_template, flash, redirect, url_for
import auth
import model

# ########
# Routing
# ########

@app.route('/lesson/')
@auth.login_required
def lesson():
    section_dbs = model.Section.query()
    return render_template(
        'lesson.html',
        html_class='lesson',
        title='Lessons',
        sections=section_dbs
        )
