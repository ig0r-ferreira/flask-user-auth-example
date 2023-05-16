from flask import Flask, redirect, render_template, request, url_for

from flask_user_auth.database import User, db


def init_app(app: Flask) -> None:
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            new_user = User(**request.form.to_dict())
            db.session.add(new_user)
            db.session.commit()
            return render_template('secrets.html', username=new_user.name)

        return render_template('register.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/secrets')
    def secrets():
        print(request.args)
        return render_template('secrets.html')

    @app.route('/logout')
    def logout():
        pass

    @app.route('/download')
    def download():
        pass
