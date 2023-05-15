from flask import Flask, render_template


def init_app(app: Flask) -> None:
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/register')
    def register():
        return render_template('register.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/secrets')
    def secrets():
        return render_template('secrets.html')

    @app.route('/logout')
    def logout():
        pass

    @app.route('/download')
    def download():
        pass
