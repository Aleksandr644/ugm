from app import app
from flask import render_template, flash, redirect, url_for
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
    if form.validate_on_submit(): #реагирует на метод POST и возвращает True
        # показываем сообщение пользователю через метод в форме get_flashed_message()
        flash("Login requested for user {}, remember_me={}".format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Авторизация', form=form) # если получили метод GET