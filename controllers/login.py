import static.login.logpass
from app import app
from flask import render_template, request, session
import pandas as pd


@app.route('/', methods=['get', 'post'])
def login():

    if request.values.get('login'):
        login_name = str(request.values.get('login'))
        login_pass = str(request.values.get('pass'))
        df_login_dict = static.login.logpass.login_dict
        for i in df_login_dict:
            if i == login_name and df_login_dict.get(i) == login_pass:
                f = 2
                break
            else:
                f = 1
    else:
        f = 1

    html = render_template(
        'login.html',
        flag = f
    # discription = df_desc_dict,
    # combo_box = df_spec,
    # image = image,
    # idTrainerSpec = session['idTrainerSpec'],
    # len = len
    )
    return html