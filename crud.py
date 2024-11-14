from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename

import cs304dbi as dbi

conn = dbi.connect()
curs = dbi.dict_cursor(conn)

def insert_movie(conn, tt, title, year, director):
    
    sql = 'select * from movie where tt = %s'
    curs.execute(sql,[tt])
    result = curs.fetchone()
    if result:  
        flash("Cannot insert movie, ID already exist in database")
    else:
        sql = 'insert into movie (tt, title, `release`, director, addedby) values (%s,%s, %s, %s, %s)'
        curs.execute(sql,[tt, title, year, director, 10027])
        # why isnt this working
        conn.commit()
    return tt

def update_render(tt):
    sql = 'select * from movie where tt = %s'
    curs.execute(sql,[tt])
    return_dic =  curs.fetchone()
    
    if return_dic.get("director"):
        sql_director = 'select name from person where nm = %s'
        curs.execute(sql_director,return_dic["director"])
        director_dic = curs.fetchone()
        return_dic.update(director_dic)
    else:
        return_dic["director"] = ""
        return_dic["name"] = "None"
    return return_dic

def update(tt, new_id, title, release, addedby, director):
    sql = 'select * from movie where tt = %s'
    curs.execute(sql, [new_id])
    result = curs.fetchone()

    #if movie already exists
    if result and new_id != tt:
        flash("Movie id already in use")
    else:
        update_helper(new_id, title, release, addedby, director, tt)
        tt = new_id
    return tt

def update_helper(tt, title, release, addedby, director, old_id):
    curs.execute("select * from staff where uid = %s", addedby)
    staff_exists = curs.fetchone()
    if director != "" and staff_exists:
        sql = 'UPDATE movie SET title = %s, tt = %s, `release` = %s, addedby = %s, director = %s where tt = %s'            
        curs.execute(sql,[title, tt, release, addedby, director, old_id])
        conn.commit()
    elif director != "" and not staff_exists:
        flash("Staff does not exist")
        sql = 'UPDATE movie SET title = %s, tt = %s, `release` = %s, director = %s where tt = %s'
        curs.execute(sql,[title, tt, release, director, old_id])
        conn.commit()
    elif staff_exists:
        sql = 'UPDATE movie SET title = %s, tt = %s, `release` = %s, addedby = %s where tt = %s'
        curs.execute(sql,[title, tt, release, addedby, old_id])
        conn.commit()
def delete(tt):
    sql = 'delete from movie where tt = %s'  
    curs.execute(sql,tt)
    conn.commit()     


