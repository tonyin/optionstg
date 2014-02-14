# -*- coding: utf-8 -*-

from main import app
from flask.ext import wtf
from flask import render_template, flash, redirect, url_for
import auth
from model import Piece

# ########
# Globals
# ########


# ######
# Forms
# ######
class PieceForm(wtf.Form):
    lesson = wtf.IntegerField('Lesson', [wtf.validators.NumberRange(min=0, max=5)])
    section = wtf.IntegerField('Section', [wtf.validators.NumberRange(min=1, max=9)])
    tag = wtf.StringField('Tag', [wtf.validators.required()])
    number = wtf.IntegerField('Number', [wtf.validators.NumberRange(min=1, max=9)])
    content = wtf.TextAreaField('Content', [wtf.validators.optional()])

# ################
# Routing - Admin
# ################

@app.route('/piece/view/')
@auth.admin_required
def piece_view():
    piece_dbs = Piece.query().order(Piece.lesson, Piece.section, Piece.number)
    return render_template(
        'piece_view.html',
        html_class='piece-view',
        title='Pieces',
        pieces=piece_dbs,
    )

@app.route('/piece/create/', methods=['GET', 'POST'])
@auth.admin_required
def piece_create():
    form = PieceForm()
    if form.validate_on_submit():
        piece_db = Piece(
            lesson = form.lesson.data,
            section = form.section.data,
            tag = form.tag.data,
            number = form.number.data,
            content = form.content.data,
        )
        try:
            piece_db.put()
            flash(u'Piece id %s successfully saved.' % piece_db.key.id(), 'success')
            return redirect(url_for('piece_view'))
        except:
            flash(u'Something went wrong.', 'info')
            return redirect(url_for('piece_update'))
    return render_template(
        'piece_update.html',
        html_class='piece-create',
        title='Create Piece',
        form=form)

@app.route('/piece/<int:piece_id>/delete/', methods=['GET', 'POST'])
@auth.admin_required
def piece_delete(piece_id):
    piece_db = Piece.get_by_id(piece_id)
    try:
        piece_db.key.delete()
        flash(u'Piece id %s successfully deleted.' % piece_id, 'success')
        return redirect(url_for('piece_view'))
    except:
        flash(u'Something went wrong.', 'info')
        return redirect(url_for('piece_view'))

@app.route('/piece/<int:piece_id>/update/', methods=['GET', 'POST'])
@auth.admin_required
def piece_update(piece_id):
    piece_db = Piece.get_by_id(piece_id)
    form = PieceForm(obj=piece_db)
    if form.validate_on_submit():
        form.populate_obj(piece_db)
        try:
            piece_db.put()
            flash(u'Piece id %s successfully saved.' % piece_db.key.id(), 'success')
            return redirect(url_for('piece_view'))
        except:
            flash(u'Something went wrong.', 'info')
            return redirect(url_for('piece_view'))
    return render_template(
        'piece_update.html',
        html_class='piece-update',
        title='Edit Piece',
        form=form,
        piece_db=piece_db
    )
