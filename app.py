from flask import render_template, url_for, redirect, request, session
from Forms import RegistrationForm, LoginForm, SearchForm, GifForm, FilterForm
from flask_bootstrap import Bootstrap
from flask_login import login_user, login_required, logout_user, current_user
from Models import User, UserGif, db
from flask_bcrypt import Bcrypt
import GiphyServices
import create

app = create.create_app()
login_manager = create.create_login_manager(app)
bcrypt = Bcrypt(app)
Bootstrap(app)


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)


@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm(csrf_enabled=False)

    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data,
                    password=hashed_pw,
                    authenticated=False)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home', user=session['user_id']))
    return render_template('login.html', form=form)


@app.route('/<user>/profile', methods=['GET', 'POST'])
@login_required
def home(user):
    if user == current_user.get_id():
        form = FilterForm()

        if request.form.get('category') != 'all' and form.validate_on_submit():
            gifs = UserGif.query.filter(db.and_(UserGif.category == form.category.data,
                                                   UserGif.username == current_user.get_id())).all()
            return render_template('home.html', user=user, gifs=gifs, form=form)
        else:
            gifs = UserGif.query.filter_by(username=user).all()
            return render_template('home.html', user=user, gifs=gifs, form=form)
    else:
        return 'Unknown Error'


@app.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        search = form.search.data
        return redirect(url_for('get_gifs', query=search))
    return render_template('search.html', form=form)


@app.route('/results/<query>', methods=['POST', 'GET'])
@login_required
def get_gifs(query):
    form = SearchForm()
    if form.validate_on_submit():
        query = form.search.data
        return redirect(url_for('get_gifs', query=query))
    else:
        gif_links = GiphyServices.get_gifs(query)
    return render_template('results.html', gif_links=gif_links, form=form)


@app.route('/save_gif', methods=['POST'])
@login_required
def save():
    url = request.form.get('url')
    form = GifForm(urlHidden=url)
    if request.form.get('category') and form.validate_on_submit():
        user_gif = UserGif(username=session['user_id'],
                           gif_url=form.urlHidden.data,
                           category=form.category.data)
        db.session.add(user_gif)
        db.session.commit()
        return redirect(url_for('home', user=session['user_id']))
    return render_template('save.html', form=form, url=url)


@app.route('/<id>/delete')
@login_required
def delete(id):
    gif = UserGif.query.filter_by(id=id).first()
    db.session.delete(gif)
    db.session.commit()
    return redirect(url_for('home', user=session['user_id']))


if __name__ == '__main__':
    app.run(debug=True)
