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

@app.route('/select/', methods=['GET','POST'])
def select():
    result = c.select_movie()
    return render_template('select.html', result = result)
    

# This route displays all the data from the submitted form onto the rendered page
# It's unlikely you will ever need anything like this in your own applications, so
# you should probably delete this handler

@app.route('/insert/', methods=['GET','POST'])
def insert():
    if request.method == 'GET':
        return render_template('insert.html',
                               page_title='Insert movie')
    elif request.method == 'POST':
        
        movie_id = request.form.get('movie-tt')
        movie_title = request.form.get('movie-title')
        release_year = request.form.get('movie-release')
        director = None

        
        #if the three variables are not none, then continue, 
        # if are, flash and return insert template

        if movie_id == "" :
            flash("missing input: movie_id")
        if movie_title== "" :
            flash("missing input: movie_title")
        if release_year == "":
            flash("missing input: release_year")
        if movie_id == "" or movie_title== "" or release_year == "":
            return render_template('insert.html',
                               page_title='Insert movie')

        result = c.insert_movie(conn, movie_id, movie_title, release_year, director)
        return redirect(url_for('update', tt = result))
    else:
        raise Exception('this cannot happen')
    

# This route shows how to render a page with a form on it.

@app.route('/update/<tt>', methods=['GET','POST'])
def update(tt):
    if request.method == 'GET':
        result = c.update_render(tt)

    # these forms go to the formecho route
        return render_template('update.html',
                           movie_id = tt,
                           movie_title = result["title"],
                           release_year = result["release"],
                           added_by = result["addedby"],
                           director = result["director"],
                           director_name = result["name"],
                           page_title='Page with two Forms'                   
                           )
    elif request.method == 'POST':
        action = request.form.get('submit')
        print(action)
        if action == "update":
            movie_id = request.form.get('movie-tt')
            movie_title = request.form.get('movie-title')
            release_year = request.form.get('movie-release')
            addedby = request.form.get('movie-addedby')
            director = request.form.get('movie-director')
            new_tt = c.update(tt, movie_id, movie_title, release_year, addedby, director)
            return redirect(url_for('update', tt = new_tt))
        else:
            c.delete(tt)
            return redirect(url_for('index'))

    else:
        raise Exception('This cannot happen')

#Why does this work when manually testing but not with script
@app.route('/redirect_to_update/', methods=['POST'])
def redirect_to_update():
    new_tt = request.form.get('menu-tt')
    print(new_tt)
    if new_tt:
        return redirect(url_for('update', tt = new_tt))
    else:
        flash('Please select a movie to update')
        return redirect(url_for('select'))

    


if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    # set this local variable to 'wmdb' or your personal or team db
    db_to_use = 'st107_db' 
    print(f'will connect to {db_to_use}')
    dbi.conf(db_to_use)
    app.debug = True
    app.run('0.0.0.0',port)
