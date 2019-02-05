from flask import render_template, url_for, redirect, request, session
from Forms import RegistrationForm, LoginForm, SearchForm, GifForm, FilterForm
from flask_bootstrap import Bootstrap
from flask_login import login_user, login_required, logout_user, current_user
from Models import User, UserGif, db
from flask_bcrypt import Bcrypt
import GiphyServices
import Create

# Configure the application with necessary settings
app = Create.create_app()

# Create the login manager
login_manager = Create.create_login_manager(app)

# Init Bcrypt and Bootstrap extensions
bcrypt = Bcrypt(app)
Bootstrap(app)


# returns a user object when reloading a user from the session
@login_manager.user_loader
def load_user(username):
    return User.query.get(username)


@app.route('/')
def index():
    return redirect(url_for('login'))


# Handles Registration of the user.
@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm(csrf_enabled=False)
    # Validate the form
    if form.validate_on_submit():
        # Hash the password for safe storage on the table
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        # Create a SQLAlchemy User Object
        user = User(username=form.username.data,
                    password=hashed_pw,
                    authenticated=False)
        # Stage and Commit the transaction
        db.session.add(user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html', form=form)


# Handles User login.
@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm(csrf_enabled=False)

    # Don't show the login page if there's an active user
    if current_user.get_id():
       return redirect(url_for('home', user=current_user.get_id()))

    # Validates the LoginForm provided
    if form.validate_on_submit():
        # Query the user table
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # Check the password if User exists
            if bcrypt.check_password_hash(user.password, form.password.data):
                # Login the user and redirect to the user profile
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home', user=session['user_id']))
    return render_template('login.html', form=form)


# Handles logout functionality (Destroys Session/clears cookie).
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Handles the user profile display.
@app.route('/<user>/profile', methods=['GET', 'POST'])
@login_required
def home(user):
    # Validate the current user can view only their own profile
    if user == current_user.get_id():
        form = FilterForm()
        # If the FilterForm was submitted and is valid, return onlt the selected category of gifs
        if request.form.get('category') != 'all' and form.validate_on_submit():
            gifs = UserGif.query.filter(db.and_(UserGif.category == form.category.data,
                                                   UserGif.username == current_user.get_id())).all()
            return render_template('home.html', user=user, gifs=gifs, form=form)
        else:
            # show all gifs on page load
            gifs = UserGif.query.filter_by(username=user).all()
            return render_template('home.html', user=user, gifs=gifs, form=form)
    else:
        # To-Do handle an unauthenticated request.
        return 'Unknown Error'


# Handles the page where you search for a Gif.
@app.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    form = SearchForm()
    # Validate the SearchForm
    if form.validate_on_submit():
        # redirect to search function
        query = form.search.data
        return redirect(url_for('get_gifs', query=query))
    return render_template('search.html', form=form)


# handles the search results page
@app.route('/results/<query>', defaults={'offset': 0}, methods=['POST', 'GET'])
@app.route('/reslults/<query>/<offset>', methods=['POST', 'GET'])
@login_required
def get_gifs(query, offset):

    # If offset is ever set to a negative value set offset to 0
    if int(offset) < 0:
        offset = 0

    form = SearchForm()
    # If there was a search on the results page,
    # validate the form and query the api with the redirect.
    if form.validate_on_submit():
        query = form.search.data
        return redirect(url_for('get_gifs', query=query))
    else:

        # return a list of gif urls to build the results page with.
        gif_links, pagination = GiphyServices.get_gifs(query, offset)

    return render_template('results.html', gif_links=gif_links, form=form,
                                           offset=pagination.offset, query=query)


# Loads the form to save a gif
@app.route('/save_gif', methods=['POST'])
@login_required
def save():
    # Takes the url from the results page to store as a
    # hidden input on the save form
    url = request.form.get('url')
    form = GifForm(urlHidden=url)
    # If the form was submitted and valid save the giff
    if request.form.get('category') and form.validate_on_submit():
        # Create an SQLAlchemy UserGif Object
        user_gif = UserGif(username=session['user_id'],
                           gif_url=form.urlHidden.data,
                           category=form.category.data)
        # Stage and commit transaction to the db
        db.session.add(user_gif)
        db.session.commit()
        return redirect(url_for('home', user=session['user_id']))
    return render_template('save.html', form=form, url=url)


# Deletes a gif from the user_gifs table.
@app.route('/<id>/delete')
@login_required
def delete(id):
    gif = UserGif.query.filter_by(id=id).first()
    db.session.delete(gif)
    db.session.commit()
    return redirect(url_for('home', user=session['user_id']))


if __name__ == '__main__':
    app.run(debug=True)
