from flask import render_template, flash, redirect, session, url_for, request, \
                  g, Markup, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
from flask_admin.base import MenuLink
from datetime import datetime
from dateutil.parser import parse
from app import app, db, lm, admin #, hashids
from .models import *
from .forms import *
from .admin import AdminModelView

admin.add_link(MenuLink(name='Back to Visitor Health Log', url='/'))
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Visitor, db.session))

def redirect_dest(fallback):
    return request.args.get('next') or fallback

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.now()
        db.session.add(g.user)
        db.session.commit()


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/')
@app.route('/index')
def index():
    if g.user.is_authenticated:
        return redirect(url_for('edit'))
    else:
        return render_template('index.html')


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    """Route to page to view and edit data"""
    # create instance of AddRowForm
    form = AddVistorForm()
    # query vistors for user
    table = Visitor.query.filter_by(user_id=g.user.id).all()
    data = []
    for row in table:
        data.append(row.__dict__)

    if request.method == 'GET':
        return render_template("edit.html", data=data, form=form)

    if form.is_submitted():
        fever = True if request.form['fever'] == 'True' else False
        symptoms = True if request.form['symptoms'] == 'True' else False
        positive_test = True if request.form['positive_test'] == 'True' else False
        quarantined = True if request.form['quarantined'] == 'True' else False
        passed = not (fever or symptoms or positive_test or quarantined)
        vistor = Visitor(
            user_id=g.user.id,
            datetime=parse(request.form['datetime']),
            purpose=request.form['purpose'],
            name=request.form['name'],
            fever=fever,
            symptoms=symptoms,
            positive_test=positive_test,
            quarantined=quarantined,
            passed=passed
        )
        db.session.add(vistor)
        db.session.commit()
        flash('Visitor added!', 'success')
        return redirect(url_for('edit'))

    return render_template('edit.html', data=data, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Route for Register Page"""
    # if user already logged in, redirect to main page
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()

    if request.method == 'GET':
        return render_template('register.html', form=form)

    # validate form submission
    if form.validate_on_submit():
        email = request.form['email']
        apartment = request.form['apartment']
        password = request.form['password']
        u = User(email, apartment, password, 1, datetime.now())
        db.session.add(u)
        db.session.commit()
        login_user(u)
        flash('Thank you for signing up!','success')
        return redirect(url_for('edit'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Route for Login Page"""
    # if user already logged in, redirect to main page
    if g.user is not None and g.user.is_authenticated:
        return redirect(redirect_dest(url_for('index')))

    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', form=form)

    # validate form submission
    if form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']
        # check if eid is in user db, add to db if not
        u = User.query.filter_by(email=email).first() #pylint: disable=invalid-name
        if u is None:
            flash('Email not found','danger')
            return redirect(url_for('login'))
        elif u.check_password(password):
            if u.login_ct is None:
                u.login_ct = 1
            else:
                u.login_ct += 1
            u.last_login = datetime.now()
            db.session.add(u)
            db.session.commit()
            login_user(u)
            return redirect(redirect_dest(url_for('edit')))
        else:
            flash('User name or password incorrect','danger')
            return redirect(redirect_dest(url_for('login')))


    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
