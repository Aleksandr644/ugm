from app import app
from flask import render_template, flash, redirect
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    posts = [{
        'author': {'nickname': 'John'},
        'body': 'Beautiful day in Portland!'
    },{
        'author': {'nickname': 'Susan'},
        'body': 'The Avengers movie was so cool!'
    }]
    user = {'nickname': 'Aleksandr644'}
    return render_template("index.html", title = 'Главная страница', user = user, posts = posts)

@app.route('/user/<path:username>')
def show_user(username):
    user = {'nickname': username}
    return render_template('index.html', title = 'Профиль пользователя', user = user)

@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenId="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form, providers = app.config['OPENID_PROVIDERS'])