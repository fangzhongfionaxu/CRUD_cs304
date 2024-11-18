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

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = secrets.token_hex()

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def index():
    return render_template('head.html',
                           page_title='Main Page')

@app.route('/select/', methods=['GET','POST'])
def select():
    conn =dbi.connect()
    if request.method == 'GET':
        result = c.select_movie(conn)
        return render_template('select.html', result = result)
    else:
        movie_id = request.form.get('menu-tt')
        return redirect(url_for('update', tt = movie_id))

    

@app.route('/insert/', methods=['GET','POST'])
def insert():
    conn =dbi.connect()
    if request.method == 'GET':
        return render_template('insert.html',
                               page_title='Insert movie')
    elif request.method == 'POST':
        
        movie_id = request.form.get('movie-tt')
        movie_title = request.form.get('movie-title')
        release_year = request.form.get('movie-release')
        director = None
        
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

@app.route('/update/<tt>', methods=['GET','POST'])
def update(tt):
    conn = dbi.connect()
    if request.method == 'GET':
        result = c.update_render(conn,tt)
        return render_template('update.html',
                           movie_title = result["title"],
                           movie_id = tt,
                           release_year = result["release"],
                           added_by = result["addedby"],
                           director = result["director"],
                           director_name = result["name"],
                           page_title='Update Page'                   
                           )
    elif request.method == 'POST':
        action = request.form.get('submit')
        if action == "update":
            movie_id = request.form.get('movie-tt')
            movie_title = request.form.get('movie-title')
            release_year = request.form.get('movie-release')
            addedby = request.form.get('movie-addedby')
            director = request.form.get('movie-director')
            result = c.update(conn,tt, movie_id, movie_title, release_year, addedby, director)
            result2 = c.update_render(conn,tt)
  
            if result is None:
                return render_template('update.html',
                           movie_id = movie_id,
                           movie_title = movie_title,
                           release_year = release_year,
                           added_by = addedby,
                           director = director,
                           director_name = result2["name"],
                           page_title='Update Page'                   
                           )
            else:
                return render_template('update.html',
                           movie_id = result["tt"],
                           movie_title = result["title"],
                           release_year = result["release"],
                           added_by = result["addedby"],
                           director = result["director"],
                           director_name = result2["name"],
                           page_title='Update Page'                   
                           )
        else:
            c.delete(conn,tt)
            return redirect(url_for('index'))

    else:
        raise Exception('This cannot happen')

@app.route('/redirect_to_update/', methods=['POST'])
def redirect_to_update():
    new_tt = request.form.get('menu-tt')
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
