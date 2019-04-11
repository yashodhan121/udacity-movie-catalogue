from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database import Movies, Base, Movie_item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import webbrowser

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Movie Catalogue Application"

engine = create_engine('sqlite:///moviescatalogappwithlogin.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/movies/')
def showMovies():
    movie = session.query(Movies).order_by(asc(Movies.movie_type))
    return render_template('movie.html', Movie=movie)


@app.route('/movie_type/<int:movietype_id>/')
def showMovie_type(movietype_id):
    movieitem = session.query(Movie_item).filter_by(
        movie_type_id=movietype_id).all()
    moviename = session.query(Movies).filter_by(id=movietype_id).one()
    return render_template('movietype.html',
                           Movieitem=movieitem, tmovietype=moviename)


@app.route('/newmovie_type/<int:movietype_id>/')
def shownewMovie_type(movietype_id):
    movieitem = session.query(Movie_item).filter_by(
        movie_type_id=movietype_id).all()
    moviename = session.query(Movies).filter_by(id=movietype_id).one()
    return render_template('newmovietype.html',
                           Movieitem=movieitem, tmovietype=moviename)


@app.route('/newmovies/')
def shownewMovies():
    movie = session.query(Movies).order_by(asc(Movies.movie_type))
    return render_template('newmovie.html', Movie=movie)


@app.route('/movies/new/', methods=['GET', 'POST'])
def newGenre():
    if 'username' not in login_session:
        return redirect('/login')

    elif request.method == 'POST':
        newgenre = Movies(movie_type=request.form['name'],
                          user_id=login_session['user_id'])
        session.add(newgenre)
        flash('New Genre %s Successfully Created' % newgenre.movie_type)
        session.commit()
        return redirect(url_for('shownewMovies'))
    else:
        return render_template('newGenre.html')


@app.route('/movies/<int:movietype_id>/delete/',
           methods=['GET', 'POST'])
def deleteGenre(movietype_id):
    GenreToDelete = session.query(
        Movies).filter_by(id=movietype_id).one()
    Genremov = session.query(Movie_item).filter_by(
        movie_type_id=movietype_id).all()
    if 'username' not in login_session:
        return redirect('/login')
    if GenreToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() \
        {alert('You are not authorized to delete this Genre. \
        Please create your own Genre in order to delete.');\
        setTimeout(function() \
        {window.location.href = '/newmovies/';}, 1000);}\
        </script><body onload='myFunction()'>"
    if request.method == 'POST':
        for i in Genremov:
            session.delete(i)
            session.commit()
        session.delete(GenreToDelete)
        session.commit()
        return redirect(url_for('shownewMovies',
                                movietype_id=movietype_id))
    else:
        return render_template('deletegenre.html', movie=GenreToDelete)


@app.route('/movies/<int:movietype_id>/edit', methods=['GET', 'POST'])
def editGenre(movietype_id):
    editedGenre = session.query(Movies).filter_by(id=movietype_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedGenre.user_id != login_session['user_id']:
        return "<script>function myFunction() \
        {alert('You are not authorized to edit this Genre. \
        Please create your own Genre in order to edit.');\
        setTimeout(function() \
        {window.location.href = '/newmovies/';}, 1000);}\
        </script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedGenre.movie_type = request.form['name']
            return redirect(url_for('shownewMovies'))
    else:
        return render_template('editGenre.html', Genre=editedGenre)


@app.route('/movie_type/<int:movietype_id>/new', methods=['GET', 'POST'])
def addnewMovie(movietype_id):
    movieitem = session.query(Movie_item).filter_by(
        movie_type_id=movietype_id).all()
    moviename = session.query(Movies).filter_by(
        id=movietype_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if moviename.user_id != login_session['user_id']:
        return "<script>function myFunction() \
        {alert('You are not authorized to add Movie.');\
        setTimeout(function()\
        {window.location.href = '/newmovies/';}, 1000);}</script>\
        <body onload='myFunction()'>"
    if request.method == 'POST':
        newmovie = Movie_item(name=request.form['name'],
                              description=request.form['description'],
                              producer=request.form['producer'],
                              starring=request.form['starring'],
                              movie_type_id=movietype_id)
        session.add(newmovie)
        session.commit()
        return redirect(url_for('shownewMovie_type',
                                movietype_id=movietype_id))
    else:
        return render_template('addnewmovie.html',
                               movietype_id=movietype_id, Movieitem=movieitem,
                               tmovietype=moviename)


@app.route('/movie_type/<int:movietype_id><int:mov_id>/edit',
           methods=['GET', 'POST'])
def editMov(movietype_id, mov_id):
    editMov = session.query(Movie_item).filter_by(id=mov_id).one()
    Genre = session.query(Movies).filter_by(id=movietype_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if Genre.user_id != login_session['user_id']:
        return "<script>function myFunction() \
        {alert('You are not authorized to edit this Movie. \
        Please create your own Movie in order to edit.');\
        setTimeout(function()\
        {window.location.href = '/newmovies/';}, 1000);}</script>\
        <body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editMov.name = request.form['name']
        if request.form['description']:
            editMov.description = request.form['description']
        if request.form['producer']:
            editMov.producer = request.form['producer']
        if request.form['starring']:
            editMov.starring = request.form['starring']
        session.add(editMov)
        session.commit()
        flash('Movie Item Successfully Edited')
        return redirect(url_for('shownewMovie_type',
                                movietype_id=movietype_id))
    else:
        return render_template('editmov.html',
                               genre=Genre, editMov=editMov)


@app.route('/movie_type/<int:movietype_id>/<int:mov_id>/delete',
           methods=['GET', 'POST'])
def deleteMov(movietype_id, mov_id):
    Genre = session.query(Movies).filter_by(id=movietype_id).one()
    movToDelete = session.query(Movie_item).filter_by(id=mov_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if Genre.user_id != login_session['user_id']:
        return "<script>function myFunction() \
        {alert('You are not authorized to delete this Movie. Please create \
        your own Movie in order to delete.');\
        setTimeout(function() \
        {window.location.href = '/newmovies/';}, 1000);}</script><body \
        onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(movToDelete)
        session.commit()
        flash('Movie Successfully Deleted')
        return redirect(url_for('shownewMovie_type',
                                movietype_id=movietype_id))
    else:
        return render_template('deletemov.html',
                               mov=movToDelete, genre=Genre)


@app.route('/Genre/<int:movietype_id>/movie/JSON')
def GenreMovieJSON(movietype_id):
    genre = session.query(Movies).filter_by(id=movietype_id).all()
    mov = session.query(Movie_item).filter_by(
        movie_type_id=movietype_id).all()
    return jsonify(movieitem=[i.serialize for i in mov])


@app.route('/Genre/<int:movietype_id>/<int:mov_id>/JSON')
def movieJSON(movietype_id, mov_id):
    Menu_Item = session.query(Movie_item).filter_by(id=mov_id).all()
    return jsonify(Menu_Item=[r.serialize for r in Menu_Item])


@app.route('/Genre/JSON')
def genreJSON():
    genre = session.query(Movies).all()
    return jsonify(Genre=[r.serialize for r in genre])


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# GConnect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;\
    border-radius: 150px;-webkit-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        # response = make_response(json.dumps('Successfully disconnected.)
        # response.headers['Content-Type'] = 'application/json'
        response = redirect(url_for('showMovies'))
        flash("You are now logged out.")
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
