# -*- coding: utf-8 -*-

import os

from flask import render_template, flash, redirect, url_for, request, g
from flask import send_from_directory
from flask_login import login_user, logout_user, current_user, login_required

from app import app, login_manager, db
from .forms import LoginForm
from .models import User, Party

global_dic = {}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def validateAndAdd(party_name):
    party = Party.query.filter_by(name=party_name).first()
    party.votes_amount += 1
    db.session.commit()

def userVoted(id):
    user = User.query.filter_by(id_num=id).first()
    user.voted = True
    db.session.commit()



@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        validateAndAdd(request.form['party_name'])
        userVoted(global_dic['current_id'])
        return redirect(url_for('login'))

    g.user = current_user #global user parameter used by flask framwork
    parties = Party.query.all() #this is a demo comment
    return render_template('index.html',
                           title='Home',
                           user=g.user,
                           parties=parties)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        ## Validate user
        if request.form['first_name'] and request.form['last_name'] and request.form['id']:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            global_dic['current_id'] = request.form['id']

            user = User.query.filter_by(id_num=global_dic['current_id']).first()
            if user and user.first_name == first_name and user.last_name == last_name:
                if user.voted is False:
                    login_user(user)  ## built in 'flask login' method that creates a user session
                    return redirect(url_for('index'))
            else:  ##validation error
                error = u'המצביע אינו מופיע במערכת'
        else:
            error = u'חסרים הנתונים, נא הזן את כל השדות'

    return render_template('login.html',
                           error=error)


## will handle the logout request
@app.route('/logout')
@login_required
def logout():
    logout_user() ## built in 'flask login' method that deletes the user session
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
