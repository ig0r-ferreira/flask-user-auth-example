from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask.typing import ResponseReturnValue
from flask_login import login_required, login_user, logout_user

from flask_user_auth.database import User, db


def init_app(app: Flask) -> None:
    @app.route('/')
    def home() -> ResponseReturnValue:
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register() -> ResponseReturnValue:
        if request.method == 'POST':
            form_data = request.form.to_dict()
            email = form_data.get('email')

            user = User.get_by_email(email)

            if not user:
                new_user = User(**form_data)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)

                return redirect(url_for('secrets'))

            flash(
                "You've already registered with this email, please login.",
                'error',
            )

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login() -> ResponseReturnValue:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.get_by_email(email)

            if not user:
                flash('This user does not exist, please try again.', 'error')
            elif not user.is_correct_password(password):
                flash('Password incorrect, please try again.', 'error')
            else:
                login_user(user)
                return redirect(url_for('secrets'))

        return render_template('login.html')

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
