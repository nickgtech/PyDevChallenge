from flask import Flask, render_template, flash, request, url_for, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from base import Base, engine, session
from user import User
from LoginForm import LoginForm

app = Flask(__name__)

app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdqyI0UAAAAAPHGB46kWdKsoR_AGld2ZZTR3Xbo'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdqyI0UAAAAAO4vjAs7b69ETiPhebt2bA6fnaRd'

Base.metadata.create_all(engine)

@app.route('/index')
def index():
    return "Hello World"

@app.route('/register/user', methods=['GET', 'POST'])
def ggiphy_register():

    form = LoginForm(csrf_enabled=False)

    if form.validate_on_submit():
        print(form.username.data)
        user = User(form.password.data,
                    form.username.data,
                    form.email.data,
                    False )
        session.add(user)
        session.commit()
        return redirect('/index')

    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)