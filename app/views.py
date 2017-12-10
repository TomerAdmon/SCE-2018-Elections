# -*- coding: utf-8 -*-

import os

from flask import render_template, flash, redirect, url_for, request, g, flash
from flask import send_from_directory
from flask_login import login_user, logout_user, current_user, login_required

from app import app, login_manager, db
from .forms import LoginForm
from .models import User, Party


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def validateAndAdd(party_name):
    ## implement me!
    pass


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        validateAndAdd(request.form['party_name'])
        User.query.filter_by(id=current_user.id).update(dict(isVoted=1))
        party_rec = Party.query.filter_by(name=request.form['party_name']).first()
        party_rec.sum += 1
        db.session.commit()
        flash(u'הצבעתך נקלטה בהצלחה', 'success')
        return render_template('login.html')
    g.user = current_user
    parties = Party.query.all()
    return render_template('index.html', title='Home', user=g.user, parties=parties)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    errFlag = False;
    if request.method == 'POST':
        if request.form['first_name'] == "" or request.form['last_name'] == "" or request.form['id_num'] == "":
            flash(u'אנא מלא את כל השדות', 'danger')
            errFlag = True;

        if errFlag:
            return render_template('login.html')
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        id_num = request.form['id_num']

        user = User.query.filter_by(first_name=first_name, last_name=last_name, id_num=id_num).first()

        if not user:
            flash('The user is not registered!', 'danger')
            return render_template('login.html')
        else:
            if user.role == 1:
                login_user(user)
                return redirect("/admin")
        if user.isVoted == 0:
            login_user(user)
            return redirect(url_for('index'))
        flash(u'משתמש זה הצביע כבר', 'danger')
        return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()  ## built in 'flask login' method that deletes the user session
    return redirect(url_for('index'))


## secret page that shows the user name
@app.route('/secret', methods=['GET'])
@login_required
def secret():
    return 'This is a secret page. You are logged in as {} {}'.format(current_user.first_name, current_user.last_name)


## will handle the site icon - bonus 2 points for creative new icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
