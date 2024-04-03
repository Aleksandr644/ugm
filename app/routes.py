from app import app, db
from flask import render_template, flash, redirect, url_for, request
from .forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Person
#from werkzeug.urls import url_parse !!! устарело
from urllib.parse import urlparse

@app.route('/')
@app.route('/index')
@login_required # защищает страницу от неавторизованных пользователей (flask_login)
def index():
    posts = [{
        'author': {'nickname': 'John'},
        'body': 'Beautiful day in Portland!'
    },{
        'author': {'nickname': 'Susan'},
        'body': 'The Avengers movie was so cool!'
    }]
    user = {'nickname': 'Aleksandr644'}
    return render_template("index.html", title = 'Главная страница', posts = posts)

@app.route('/user/<path:username>')
def show_user(username):
    user = {'nickname': username}
    return render_template('index.html', title = 'Профиль пользователя', user = user)

@app.route('/login', methods = ['GET','POST'])
def login():
    
    if current_user.is_authenticated:   # Возвращает тру если юзер авторизован
        return redirect(url_for("index"))   # перенаправляет на главную страницу
    form = LoginForm()  # инициализирует форму авторизации
    if form.validate_on_submit():   # проверяет на POST т.е. нажатие
        user = Person.query.filter_by(login=form.username.data).first() # юзер обьект из БД(читаем через обратный вызов загрузчика пользователя)
        if user is None or not user.check_password(form.password.data): # если пользователь не найден или проверяем пароль
            flash("Неправильный Login или Pasword") # даем ответ
            return redirect(url_for('login'))   #  перенаправляет обратно на страницу авторизации
        login_user(user, remember=form.remember_me.data)    # регистрация пользователя во время входа в систему, для всех страниц будет переменная current_user
        next_page = request.args.get('next') # получаем страницу к которой хотел обратиься пользователь
        if not next_page or urlparse(next_page).netloc != '': #  если страница отсутствует или домен не пуст
            # пояснение к netlock: для большей безопасности, что бы злоумышленник не перенаправлял на сторонние сайты
            next_page = url_for('index')
        return redirect(next_page)   # перенаправление
    return render_template("login.html", title="Авторизация", form=form)    # создание страницы по форме

@app.route('/logout') 
def logout():
    logout_user() # сброс регистрации пользователя
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Person(login=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Поздравляю! Вы зарегистрированы как {form.username.data}")
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)