# -*- coding: utf-8 -*-

from flask import flash

lesson_0 = {1:'b', 2:'c', 3:'a', 4:'c', 5:'a'}

def check(answers, lesson):
    
    if lesson == 0:
        if len(answers) != len(lesson_0):
            flash(u'Please answer all the questions.')
            return False
        for i in answers:
            if answers[i] != lesson_0[int(i)]:
                flash(u'Question ' + i + ' is incorrect.', 'error')
                return False
    
    return True
