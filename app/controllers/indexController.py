from util import db;
from flask import flash, redirect, render_template, request, session, url_for;

from emailHelper import send_mail;
from forms import RegisterForm, LoginForm;
from models import User;

def index():
    return render_template('index.html');



def register():
    form = RegisterForm.RegisterForm();

    if request.method == 'POST' and form.validate_on_submit():
        user = User.User(
            username   = form.username.data,
            email      = form.email.data,
            password   = form.password.data,
            first_name = form.first_name.data,
            last_name  = form.last_name.data
        );

        db.session.add(user);
        db.session.commit();

        send_mail(recipients = [form.email.data],
                  subject    = 'Welcome to ...',
                  template   = 'mail/confirmRegistration',
                  user       = user,
                  token      = user.create_confirm_token(),
                 );

        # TODO: should be redirect to confirm registration page.
        return redirect(url_for('index.index'));

    return render_template('register.html', form=form);



def confirmRegistration(token):
    user = User.User();
    data = user.validate_confirm_token(token);

    if data:
        user = User.User.query.filter_by(user_id=data.get('user_id')).first();
        user.confirm = True;
        db.session.add(user);
        db.session.commit();
        return 'Thands For Your Activate';
    else:
        return 'wrong token';



def login():
    form = LoginForm.LoginForm();

    if request.method == 'POST' and form.validate_on_submit():
        user = User.User.query.filter_by(username=form.username.data).first();
        session.clear();
        session['user_id'] = user.user_id;
        return redirect(url_for('index.index'));

    return render_template('login.html', form=form);

def logout():
    session.clear();
    return redirect(url_for('index.index'));