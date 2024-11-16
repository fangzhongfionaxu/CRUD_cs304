from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename

import cs304dbi as dbi



def insert_movie(conn, tt, title, year, director):
    curs = dbi.dict_cursor(conn)
    sql = 'select * from movie where tt = %s'
    curs.execute(sql,[tt])
    result = curs.fetchone()
    if result:  
        flash("Cannot insert movie, ID already exist in database")
    else:
        sql = 'insert into movie (tt, title, `release`, director, addedby) values (%s,%s, %s, %s, %s)'
        curs.execute(sql,[tt, title, year, director, 10027])
        conn.commit()
    return tt

def update_render(conn, tt):
    curs = dbi.dict_cursor(conn)
    sql = 'select * from movie where tt = %s'
    print(tt)
    curs.execute(sql,[tt])
    return_dic =  curs.fetchone()
    print("In update render")
    print(return_dic)
    if return_dic.get("director"):
        sql_director = 'select name from person where nm = %s'
        curs.execute(sql_director,return_dic["director"])
        director_dic = curs.fetchone()
        return_dic.update(director_dic)
    else:
        return_dic["director"] = ""
        return_dic["name"] = "None"
    print(return_dic)
    return return_dic

def update(conn, tt, new_id, title, release, addedby, director):
    curs = dbi.dict_cursor(conn)
    if tt != new_id:
        sql = 'select * from movie where tt = %s'
        curs.execute(sql, [new_id])        
        result = curs.fetchone()
        if result:
            flash("Movie id already in use")
            return None
        else:
            update_helper(conn, new_id, title, release, addedby, director, tt)
            tt = new_id
    else:
        update_helper(conn, tt, title, release, addedby, director, tt)
    sql = 'select * from movie where tt = %s'
    curs.execute(sql, [tt])
    result = curs.fetchone()
    print("Result at end of update")
    print(result)
    return result

def update_helper(conn, tt, title, release, addedby, director, old_id):
    curs = dbi.dict_cursor(conn)
    print("In update helper")
    print(director)
    if director != "":
        sql = 'UPDATE movie SET title = %s, tt = %s, `release` = %s, addedby = %s, director = %s where tt = %s'            
        curs.execute(sql,[title, tt, release, addedby, director, old_id])
        conn.commit()
    else:
        sql = 'UPDATE movie SET title = %s, tt = %s, `release` = %s, addedby = %s where tt = %s'
        curs.execute(sql,[title, tt, release, addedby, old_id])
        conn.commit()

def delete(conn,tt):
    curs = dbi.dict_cursor(conn)
    sql = 'delete from movie where tt = %s'  
    curs.execute(sql,tt)
    conn.commit()     

def select_movie(conn):
    curs = dbi.dict_cursor(conn)
    sql = 'SELECT tt, title FROM movie WHERE `release` IS NULL OR director IS NULL'
    curs.execute(sql)
    result = curs.fetchall()
    return result


