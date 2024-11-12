from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename

import cs304dbi as dbi

conn = dbi.connect()
curs = dbi.dict_cursor(conn)

def insert_movie(conn, tt, title, year):
    
    sql = 'select * from movie where tt = %s'
    curs.execute(sql,[tt])
    result = curs.fetchone()
    
    if result:  
        flash("Cannot insert movie, ID already exist in database")
    else:
        sql = 'insert into movie (tt, title, `release`,addedby) values (%s,%s, %s, %s)'
        curs.execute(sql,[tt, title, year, 10027])
        conn.commit()
    sql_select = 'select * from movie where tt = %s'
    curs.execute(sql_select, [tt])
    
    return curs.fetchone()

def update(tt):
    sql = 'select * from movie where tt = %s'
    curs.execute(sql,[tt])
    return_dic =  curs.fetchone()
    
    if return_dic["director"] :
        sql_director = 'select name from person where nm = %s'
        curs.execute(sql_director,return_dic["director"])
        director_dic = curs.fetchone()
        return_dic.update(director_dic)
    else:
        return_dic["name"] = "None"

    return return_dic
        


