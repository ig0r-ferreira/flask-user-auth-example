from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import Email, InputRequired, Length


class BaseForm(FlaskForm):
    @property
    def data(self):
        return {
            key: value
            for key, value in super().data.items()
            if key not in ('csrf_token', 'submit')
        }


class LoginForm(BaseForm):
    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField(
        'Password', validators=[InputRequired(), Length(min=8)]
    )
    submit = SubmitField('Sign in')


class RegisterForm(BaseForm):
    name = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField(
        'Password', validators=[InputRequired(), Length(min=8)]
    )
    submit = SubmitField('Sign up')
