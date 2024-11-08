from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)

# one or the other of these. Defaults to MySQL (PyMySQL)
# change comment characters to switch to SQLite

import cs304dbi as dbi
import crud as c
# import cs304dbi_sqlite3 as dbi

import secrets

conn =dbi.connect()

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = secrets.token_hex()

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def index():
    return render_template('head.html',
                           page_title='Main Page')

# You will probably not need the routes below, but they are here
# just in case. Please delete them if you are not using them

@app.route('/select/', methods=["GET", "POST"])
def select():
    if request.method == 'GET':
        return render_template('select.html',
                               page_title='Form to collect username')
    else:
        try:
            username = request.form['username'] # throws error if there's trouble
            flash('form submission successful')
            return render_template('greet.html',
                                   page_title='Welcome '+username,
                                   name=username)

        except Exception as err:
            flash('form submission error'+str(err))
            return redirect( url_for('index') )

# This route displays all the data from the submitted form onto the rendered page
# It's unlikely you will ever need anything like this in your own applications, so
# you should probably delete this handler

@app.route('/insert/', methods=['GET','POST'])
def insert():
    if request.method == 'GET':
        return render_template('insert.html',
                               page_title='Insert movie')
    elif request.method == 'POST':
        #i

        #if tt exist in db, then flash
        #else insert new movie to db
        
        
        movie_id = request.form.get('movie-tt')
        movie_title = request.form.get('movie-title')
        release_year = request.form.get('movie-release')
        print("test")
        print(movie_title)
        
        #if the three variables are not none, then continue, 
        # if are, flash and return insert template

        # should this be None or "" if I changed request.form to request.form.get
        # why is the if statement not working
        if movie_id == None :
            flash("missing input: movie_id")
        if movie_title== None :
            flash("missing input: movie_title")
        if release_year == None:
            flash("missing input: release_year")
        if movie_id == None or movie_title== None or release_year == None:
            render_template('insert.html',
                               page_title='Insert movie')

        result = c.insert_movie(conn, movie_id, movie_title, release_year)
        #select * from movie where tt = movie_id
        title = result["title"]
        movie_id = result["tt"]
        release_year = result["release"]
        addedby = result["addedby"]
        director_id = result["director"]

        return redirect(url_for('update', tt = movie_id))
    else:
        raise Exception('this cannot happen')
    

# This route shows how to render a page with a form on it.

@app.route('/update/<int:tt>', methods=['GET','POST'])
def update(tt):
    # these forms go to the formecho route
    return render_template('update.html',
                           movie_id = tt,
                           page_title='Page with two Forms'                   
                           )


if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    # set this local variable to 'wmdb' or your personal or team db
    db_to_use = 'fx100_db' 
    print(f'will connect to {db_to_use}')
    dbi.conf(db_to_use)
    app.debug = True
    app.run('0.0.0.0',port)
