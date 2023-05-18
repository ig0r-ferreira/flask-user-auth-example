from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    send_from_directory,
    url_for,
)
from flask.typing import ResponseReturnValue
from flask_login import login_required, login_user, logout_user

from flask_user_auth.database import User, db
from flask_user_auth.forms import LoginForm, RegisterForm


def init_app(app: Flask) -> None:
    @app.route('/')
    def home() -> ResponseReturnValue:
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register() -> ResponseReturnValue:
        form = RegisterForm()

        if form.validate_on_submit():
            user = User.get_by_email(form.email.data)

            if not user:
                new_user = User(**form.data)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)

                return redirect(url_for('secrets'))

            flash(
                "You've already registered with this email, please login.",
                'error',
            )

        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login() -> ResponseReturnValue:
        form = LoginForm()

        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.get_by_email(email)

            if not user:
                flash('This user does not exist, please try again.', 'error')
            elif not user.is_correct_password(password):
                flash('Password incorrect, please try again.', 'error')
            else:
                login_user(user)
                return redirect(url_for('secrets'))

        return render_template('login.html', form=form)

    @app.route('/secrets')
    @login_required
    def secrets() -> ResponseReturnValue:
        return render_template('secrets.html')

    @app.route('/logout')
    @login_required
    def logout() -> ResponseReturnValue:
        logout_user()
        return redirect(url_for('home'))

    @app.route('/download')
    @login_required
    def download() -> ResponseReturnValue:
        return send_from_directory(
            'static', 'files/cheat_sheet.pdf', as_attachment=True
        )
