from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    """Formulário de login."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    """Formulário de registro."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[
        DataRequired(),
        Length(min=6, message='A senha deve ter pelo menos 6 caracteres')
    ])
    confirm_password = PasswordField('Confirmar Senha', validators=[
        DataRequired(),
        EqualTo('password', message='As senhas devem ser iguais')
    ])
    submit = SubmitField('Registrar')
