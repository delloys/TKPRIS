from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import *
import pandas as pd


@app.route('/index', methods=['get', 'post'])
def index():
    con = get_db_connection()

    book_name = ''
    author = -1
    tom = ''
    year = -1
    desc = ''
    annot = ''
    id_book = -1
    type = -1
    rasp = ''
    tag = -1
    link = ''
    old_author = -1

    if request.values.get('id_book'):
        id_book = request.values.get('id_book')

    if request.values.get('confirm'):
        book_name = request.values.get('new_name')
        author = request.values.get('new_authors')
        tom = request.values.get('new_tom')
        year = request.values.get('new_year')
        count_book = request.values.get('new_kol_vo')
        desc = request.values.get('new_desc')
        annot = request.values.get('new_annot')
        type = request.values.get('type')
        tag = request.values.get('tag')
        rasp = request.values.get('new_rasp')
        link = request.values.get('new_link')
        old_author = request.values.get('old_author')
        df_change_bok = change_book(con, book_name, annot, desc, type, id_book, tom, int(year), rasp, tag, int(author),
                                    link, int(old_author))

    df_old_author = get_old_author(con, id_book)
    df_books = get_books(con)
    df_select_book = get_selected_book(con, id_book)
    df_tag = get_tag(con)
    df_type = get_type(con)
    df_author = get_authors2(con)

    if request.values.get('new_in_authors'):
        new_in_authors = request.values.get('new_in_authors')
        new_in_name = request.values.get('new_in_name')
        new_in_tom = request.values.get('new_in_tom')
        new_in_year = request.values.get('new_in_year')
        new_in_tag = int(request.values.get('new_in_tag'))
        new_in_type = int(request.values.get('new_in_type'))
        new_in_rasp = str(request.values.get('new_in_rasp'))
        str2 = new_in_rasp.split(' ')
        new_closet = str2[1]
        new_shelf = str2[3]
        new_in_link = request.values.get('new_in_link')
        new_in_desc = request.values.get('new_in_desc')
        new_in_annot = request.values.get('new_in_annot')
        new_book = get_new_book(con,new_in_name,new_in_annot,new_in_desc,new_in_type)
        new_author = get_new_author(con, new_in_authors)
        get_new_book_author(con,new_book,new_author)
        new_storage = gen_new_storage(con,new_closet,new_shelf,new_in_link)
        gen_new_copy(con,new_in_year,new_in_tom,new_book,new_storage)
        if new_in_tag != '':
            gen_new_book_tag(con,new_in_tag,new_book)
        else:
            a=1
    elif request.values.get('search'):
        aut = request.values.get('search_in_author')
        t = request.values.get('search_in_tag')
        typ = request.values.get('search_in_type')

        df_books = search(con,aut,t,typ)
    else:
        a=1
        df_books = get_books(con)






    df_tags = get_tags(con)
    df_types = get_types(con)
    df_authors = get_authors(con)

    session['ID_Tag'] = 1
    session['ID_Type'] = 1
    session['ID_Author'] = 1

    html = render_template(
        'index.html',
        ID_Author = session['ID_Author'],
        ID_Tag= session['ID_Tag'],
        ID_Type = session['ID_Type'],
        combo_authors=df_authors,
        combo_tags = df_tags,
        combo_types = df_types,
        books = df_books,
        len=len,
        id_book=id_book,
        select_book=df_select_book,
        tags=df_tag,
        types=df_type,
        authors=df_author,
        old_author=df_old_author,
        int=int
        )

    return html