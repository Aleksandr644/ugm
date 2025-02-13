from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegistrationForm, CreateBidForm, BidCommentForm, BidsForm, ChangeForm, ProductsForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import Customers, Bids, Comments, Products
from flask import request
from urllib.parse import urlsplit
from datetime import datetime, timezone

button_index = {"href":"/index", "name":"Главная\nстраница"}
button_about = {"href":"/about", "name":"О нас"}
button_registration = {"href":"/registration", "name":"Регистрация"}
button_login = {"href":"/login", "name":"Личный кабинет"}
button_user = {"href":"/user", "name":"Профиль"}
button_product = {"href":"/products", "name":"Склад"}
button_bid = {"href":"/bid", "name":"Заявка"}
button_bids = {"href":"/bids", "name":"Заявки"}
button_create = {"href":"/create", "name":"Создание\nзаявки"}
button_exit = {"href":"/logout", "name":"Выход"}

def create_buttons():
    button = []    
    if current_user.is_authenticated:
        button.append(button_create)
        button.append(button_user)
        if db.session.scalar(sa.select(Customers).where(Customers.id == current_user.get_id())).employee:
            button.append(button_product)
            button.append(button_bids)
        button.append(button_exit)  
    else:
        button.append(button_index)
        button.append(button_about)
        button.append(button_login)
    return button

#главная страница
@app.route('/')
@app.route('/index')
def index():
    title = 'Главная страница'
    button = create_buttons()
    return render_template('index.html', title=title, buttons=button)

# о нас
@app.route('/about')
def about():
    title = 'О нас'  
    button = create_buttons()
    return render_template('about.html', title=title, buttons=button)

# регистрация
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated and not current_user.administrator:
        return redirect(url_for('index'))
    title = 'Регистрация'
    button = create_buttons()
    form=RegistrationForm()
    if form.validate_on_submit():
        user = Customers(login=form.username.data, email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data, phone=form.phone.data, employee=form.employee.data, administrator=form.administrator.data, description=form.description.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(F"Поздравляю, Вы зарегистрированы в системе под логином {form.username.data}")
        if form.employee.data:
            flash(f"Право работника {form.employee.data}, права администратора {form.administrator.data}")
        return redirect(url_for('login'))
    return render_template('registration.html', title=title, buttons=button, form=form)

# авторизация
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = 'Авторизация'
    form = LoginForm()
    button = create_buttons()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(Customers).where(Customers.login == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Неправильные логин или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title=title, buttons=button, form=form)

# пользователь
@app.route('/user')
@login_required
def empty_user():
    return redirect(url_for("user", id=current_user.id))

@app.route('/user/<id>')
@login_required
def user(id):
    if current_user.id != int(id) and not current_user.employee:
        return redirect(url_for("user", id=current_user.id))
    title = 'Профиль'
    button = create_buttons()    
    user = db.session.get(Customers, int(id))
    bids  = db.session.query(Bids).filter(Bids.customer == user).order_by(sa.desc(Bids.id))
    bids_count = bids.count()
    bids_open = bids.filter(Bids.date_close == None).count()
    page = request.args.get('page', 1, type=int)
    bids_page = db.paginate(bids, page=page, per_page=10, error_out=False)
    next_url = url_for('user', id=user.id, page=bids_page.next_num) if bids_page.has_next else None
    prev_url = url_for('user', id=user.id, page=bids_page.prev_num) if bids_page.has_prev else None
    print(f"next_url: {next_url}, prev_url: {prev_url}")
    return render_template('user.html', title=title, buttons=button, bids=bids_page.items, next_url=next_url, prev_url=prev_url, bids_count=bids_count, bids_open=bids_open, user=user )

# склад
@app.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    title = 'Склад'
    button = create_buttons()
    form = ProductsForm()
    product = None
    if form.validate_on_submit():
        if form.name.data:
            name = f'%{form.name.data}%'
            product = db.session.query(Products).filter(Products.name.like(name))
    if not product:
        product = db.session.query(Products).order_by(sa.desc(Products.id))
    page = request.args.get('page', 1, type=int)
    product_page = db.paginate(product, page=page, per_page=10, error_out=False)
    next_url = url_for('products', page=product_page.next_num, ) if product_page.has_next else None
    prev_url = url_for('products', page=product_page.prev_num, ) if product_page.has_prev else None
    return render_template('products.html', title=title, buttons=button, products=product_page.items, prev_url=prev_url, next_url=next_url, form=form)

# каталог заявок
@app.route('/bids', methods=['GET', 'POST'])
@login_required
def bids():
    title = 'Каталог заявок'
    form = BidsForm()
    if not current_user.employee:
        return redirect(url_for("user", id=current_user.id))
    if form.validate_on_submit():
        if form.id.data:
            return redirect(url_for('bid', id=form.id.data))
        elif form.open.data:
            return redirect(url_for('bids',open=form.open.data))
        return redirect(url_for('bids'))
    button = create_buttons()
    bids  = db.session.query(Bids).order_by(sa.desc(Bids.id))
    r_open = request.args.get('open', 'False', type=str)
    if r_open =='True':
        flash('Только открытые')
        bids = bids.filter(Bids.date_close == None)
    date = request.args.get('date', 0,type=int)
    page = request.args.get('page', 1, type=int) 
    bids_page = db.paginate(bids, page=page, per_page=10, error_out=False)
    next_url = url_for('bids', page=bids_page.next_num, open=r_open) if bids_page.has_next else None
    prev_url = url_for('bids', page=bids_page.prev_num, open=r_open) if bids_page.has_prev else None
    return render_template('bids.html', title=title, form=form, buttons=button, bids=bids_page.items, next_url=next_url, prev_url=prev_url)

# тело заявки
@app.route('/bid/<id>', methods=['GET', 'POST'])
@login_required
def bid(id):
    bid = db.session.get(Bids, int(id))
    if not bid:
        flash("Заявки не существует")
        return redirect(url_for("user", id=current_user.id))
    form = BidCommentForm()
    if form.validate_on_submit():
        comment = Comments(bid_id = id, customer=current_user, description=form.text.data)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("bid", id=id))
    title = f'Заявка №{id}'
    button = create_buttons()
    user = bid.customer
    comments = db.session.query(Comments).filter(Comments.bid_id == int(id)).all()
    return render_template('bid.html', title=title, buttons=button, bid=bid, user=user, comments=comments, form=form)

# создание заявки
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    title = 'Создание заявки'
    button = create_buttons()
    form=CreateBidForm()
    if form.validate_on_submit():
        bid = Bids(description=form.description.data, customer=current_user)
        print("bid id = ", bid.id)        
        db.session.add(bid)
        db.session.commit()
        comment = Comments(bid_id=bid.id, customer=current_user, description="Заявка открыта")
        db.session.add(comment)
        db.session.commit()
        flash(f'Заявка зарегистрированна под номером {bid.id}')
        return redirect(url_for('create'))
    return render_template('create.html', title=title, buttons=button, form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
@app.route('/close/<id>')
@login_required
def close(id):
    comment = Comments(bid_id=id, customer=current_user, description="Заявка закрыта")
    db.session.add(comment)
    bid=db.session.get(Bids, int(id))
    bid.date_close = datetime.now(timezone.utc)
    db.session.commit()
    return redirect(url_for('bid', id=id))
@app.route('/open/<id>')
@login_required
def open(id):
    comment = Comments(bid_id=id, customer=current_user, description="Заявка открыта")
    db.session.add(comment)
    bid=db.session.get(Bids, int(id))
    bid.date_close = None
    db.session.commit()
    return redirect(url_for('bid', id=id))

@app.route('/change_profile', methods=["POST","GET"])
@login_required
def change_profile():
    title='Изменение провиля'
    button = create_buttons()
    form = ChangeForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.password.data):
            flash('Введите Ваш действующий пароль.')
            return redirect(url_for('change_profile'))
        else:
            user = db.session.get(Customers, int(current_user.id))
            if form.email.data and form.email.data != user.email:
                user.email = form.email.data
                flash('Почта успешно изменена')
            if form.first_name.data and form.first_name.data != user.first_name:
                user.first_name = form.first_name.data
                flash('Имя успешно изменено')
            if form.last_name.data and form.last_name.data != user.last_name:
                user.last_name = form.last_name.data                
                flash('Фамилия успешно изменена')
            if form.phone.data and form.phone.data != user.phone:
                user.phone = form.phone.data
                flash('Номер телефона успешно изменен')
            if form.description.data and form.description.data != user.description:
                user.description = form.description.data
                flash('Описание успешно изменено')
            if form.password2.data and form.password2.data == form.confirm.data:
                user.set_password(form.password2.data)                
                flash('Пароль успешно изменен')
            db.session.commit()
            return redirect(url_for('user', id=current_user.id))
    return render_template('change_profile.html', title=title, buttons=button, form=form, user=current_user)