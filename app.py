import dash
from dash import Dash, html, dcc, Input, Output, State, ctx
import pandas as pd
import plotly.graph_objects as go
import mariadb
from flask import (
    Flask,
    render_template,
    request,
    json,
    flash,
    session,
    redirect,
    url_for,
)
from flask_mail import Mail,Message
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import time
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from datetime import datetime, timedelta

# Font Awesome Icon's
external_scripts = [{'src': 'https://kit.fontawesome.com/19f1c21c33.js',
     'crossorigin': 'anonymous'}]

# Bootstrap
external_stylesheets = [{'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css',
     'rel': 'stylesheet', 'integrity': 'sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi',
     'crossorigin': 'anonymous'}]

# Initialize app
app = Dash(__name__,
           use_pages=True,
           external_scripts = external_scripts,
           external_stylesheets=external_stylesheets
           )

# Secret key
app.server.secret_key = 'purpleMap'

# App server configs
app.server.config['SECREY_KEY'] = 'purpleMap'
app.server.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.server.config['MAIL_PORT'] = 587
app.server.config['MAIL_USE_TLS'] = True
app.server.config['MAIL_USERNAME'] = 'territoriamtyy@gmail.com'
app.server.config['MAIL_PASSWORD'] = 'qmavdntlhdwommco'

# Mail server
mail=Mail(app.server)

app.index_string = '''<!DOCTYPE html>
<html>
    <head>
        <!-- Google tag (gtag.js) -->
        <script async src='https://www.googletagmanager.com/gtag/js?id=G-57PKT06DTW'></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'G-57PKT06DTW');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>'''

server = app.server

# Page layout
app.layout = html.Div(
    [
        # dash.page_container
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content', children=[]),
    ]
)

app.config['suppress_callback_exceptions'] = True

# Call to pages
from pages import (
    login,
    index,
    password_recovery,
    sent_mail,
    perceptions_map,
    page_not_found
)


# Navbar - Callback
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

app.callback(
    Output('navbar-collapse', 'is_open'),
    [Input('navbar-toggler', 'n_clicks')],
    [State('navbar-collapse', 'is_open')],
)(toggle_navbar_collapse)


# Sidebar - Callback
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

app.callback(
    Output('offcanvas', 'is_open'),
    Input('open-offcanvas', 'n_clicks'),
    [State('offcanvas', 'is_open')],
)(toggle_offcanvas)


# Map

# Access token
token = 'pk.eyJ1IjoianB6cDIwMDEiLCJhIjoiY2xmcmEzNnhyMDNjdDNycXQ0d3A2N3NjbyJ9.PUJ_q_U96vOQ94oli7JT6g'

# Map layout
map_layout = dict(
    mapbox={
        'accesstoken': token,
        'style': 'light',
        'zoom': 12,
        'center': dict(lat=25.675456439828732, lon=-100.31115409182688)
    },
    mapbox_bounds={'west': -100.6, 'east': -100.1, 'south': 25.5, 'north': 25.9},
    showlegend=False,
    margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
    modebar=dict(remove=['zoom', 'toimage', 'pan', 'select', 'lasso', 'zoomin', 'zoomout', 'autoscale', 'reset',
                         'resetscale', 'resetview']),
    hoverlabel_bgcolor='#000000'
)

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user='root', password='root', host='localhost', port=3307, database='kanan'
    )
    cur = conn.cursor()
except mariadb.Error as e:
    print(f'Error connecting to MariaDB Platform: {e}')

# Estaciones de Metro
# estaciones_metro = pd.read_csv('assets/estaciones_metro.csv')

# Reportes
reportes = pd.read_csv('assets/reportes.csv')

# Percepciones - Espacio inseguro y de peligro
cur.execute("SELECT SUBSTRING_INDEX(location,',', 1) AS lat, SUBSTR(location, POSITION(',' IN  location)+2, LENGTH(location)) AS lon FROM record WHERE type='inseguro' AND time >= DATE_SUB(NOW(), INTERVAL 3 MONTH);")
percepciones = cur.fetchall()

# Percepciones - Espacio seguro
cur.execute("SELECT SUBSTRING_INDEX(location,',', 1) AS lat, SUBSTR(location, POSITION(',' IN  location)+2, LENGTH(location)) AS lon FROM record WHERE type='seguro' AND time >= DATE_SUB(NOW(), INTERVAL 3 MONTH);")
percepciones_seguro = cur.fetchall()

mapa = go.Figure(go.Scattermapbox())
mapa.update_layout(map_layout)

# Map - Callback
@app.callback(Output('mapa-movil', 'figure'), [Input('switches-input-movil', 'value')])
@app.callback(Output('mapa-desktop', 'figure'), [Input('switches-input-desktop', 'value')])
def on_form_change(switches_value):

    mapa = go.Figure(go.Scattermapbox())

    # 911
    if 1 in switches_value:
        mapa.add_scattermapbox(
            lat=reportes['latitud'],
            lon=reportes['longitud'],
            marker={'size': 6, 'opacity': .1, 'color': '#4974a5'},
            hoverinfo='none'
        )

    # Espacios inseguros
    if 2 in switches_value:
        mapa.add_scattermapbox(
            lat=list(map(lambda x: x[0], percepciones)),
            lon=list(map(lambda x: x[1], percepciones)),
            marker={'size': 14, 'opacity': .7, 'color': '#A97BB5'},
            hoverinfo='none'
        )

    # Espacios seguros
    if 3 in switches_value:
        mapa.add_scattermapbox(
            lat=list(map(lambda x: x[0], percepciones_seguro)),
            lon=list(map(lambda x: x[1], percepciones_seguro)),
            marker={'size': 14, 'opacity': .7, 'color': '#8bb77f'},
            hoverinfo='none'
        )

    mapa.update_layout(map_layout)
    return mapa

#ACCESING PAGES

# Based on the path, returns a page's layout
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return perceptions_map.layout
    if pathname == '/login':
        if 'user' in session:
            redirect('/index')
            return index.layout
        else:
            return login.layout
    if pathname == '/password_recovery':
        if 'user' in session:
            redirect('/index')
            return index.layout
        return password_recovery.layout
    if pathname == '/index':
        if 'user' not in session:
            return login.layout
        else:
            return index.layout
    else:
        return page_not_found.layout

#Deleting records route
@app.server.route('/delete_record/<int:id>',methods=['GET'])
def page_delete_record(id):
        if 'user' not in session:
            return redirect('/page_not_found')
        else:
            cur.execute('CALL check_record(%s)',(id,))
            data=cur.fetchone()
            if data[0]:
                cur.execute('CALL get_record(%s)', (id,))
                table=cur.fetchone()
                return render_template('delete.html', record=table)
            else:
                return redirect('/page_not_found')

#When cancelling a records delete request, redirects to index
@app.server.route('/cancel')
def cancel_delete_record():
    if 'user' not in session:
            return redirect('/page_not_found')
    else:
       return redirect('/index')
    
#Delete record from the db
@app.server.route('/delete/<int:id>',methods=['POST'])
def execute_delete_record(id):
    if 'user' not in session:
        return redirect('/page_not_found')
    else:
        cur.execute('CALL delete_record(%s)',(id,))
        conn.commit()
        return render_template('/delete_alert.html')
    
#Create token: Creates the token for password recovery
def get_token(user_id): 
    serial=Serializer(app.server.config['SECREY_KEY'])
    return serial.dumps({'user_id':user_id})

#Verify token: Verifies the token for password recovery belongs to a user and is valid
def verify_token(token):
    serial=Serializer(app.server.config['SECREY_KEY'])
    try:
        user_id = serial.loads(token,max_age=600)['user_id']
    except:
        return None
    return user_id

#Route for password recovery link: If the link is valid, show the page for restoring the password
@app.server.route('/restore_password/<token>', methods=['GET','POST'])
def restore_password(token):
    user=verify_token(token)
    if user is None:
        return render_template('expired_token.html')
    return render_template('restore_password.html',user_id=user)

# Updates the password, shows succesful alert and redirects to login
@app.server.route('/restore_password/<int:id>', methods=['POST'])
def update_password(id):
    cur.execute('CALL update_password(%s,%s)',(id, request.form.get("new_password")))
    conn.commit()
    return render_template('password_updated_alert.html')
   
# LOGIN

# Checks the conditions the email has to fulfill
def check_email(email):
    if email is not None and ('@' not in email or '.' not in email or '@.' in email):
        return True
    return False


# Checks the conditions the password has to fulfill
def check_password(password):
    if password is not None and len(password) <= 0:
        return True
    return False


# Validate login form inputs : If at least one input is empty, the submit button is disabled
@app.callback(
    Output('submit_button', 'disabled'),
    [Input('email', 'value'), Input('password', 'value')],
)
def login_inputs_validation(email, password):
    if (
        email is None
        or password is None
        or check_email(email)
        or check_password(password)
    ):
        return True
    return False


# Email input feedback : If the email is not valid, feedback will be shown to the user
@app.callback(
    Output('email', 'invalid'), Input('email', 'value'), prevent_initial_call=True
)
def show_email_feedback(email):
    if check_email(email):
        return True
    return False


# Password input feedback : If the password is not valid, feedback will be shown to the user
@app.callback(
    Output('password', 'invalid'), Input('password', 'value'), prevent_initial_call=True
)
def show_password_feedback(password):
    if check_password(password):
        return True
    return False


# User credentials authentication : Checks that both credentials exist in the db to authenticate the user into the system
@app.callback(
    [Output('login_form', 'children'), Output('bad_credentials_alert', 'is_open')],
    Input('submit_button', 'n_clicks'),
    State('email', 'value'),
    State('password', 'value'),
    prevent_initial_call=True,
)
def authenticate_login(n_clicks, email, password):
    if n_clicks is not None:
        cur.execute('CALL authenticate_login(%s,%s)', (email, password))
        data = cur.fetchone()[0]
        if data:
            cur.execute('CALL user_num(%s)', (email,))
            data_id = cur.fetchone()[0]
            session['user'] = data_id
            return dcc.Location(href='/index', id='Index'), False
        else:
            return True, True
    return True, False


# INDEX (RECORDS)

# Add record modal : Allows the admin to open the modal to add a report
@app.callback(
    Output('add_record_modal', 'is_open'),
    Input('open_add_record_modal', 'n_clicks'),
    State('add_record_modal', 'is_open'),
    prevent_initial_call=True,
)
def toggle_add_record_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


# Checks the conditions the latitude has to fulfill
def check_latitude(latitude):
    if latitude is not None:
        try:
            number = float(latitude)
            if number > 90 or number < -90:
                return False
            return True
        except ValueError:
            return False
    return False


# Checks the conditions the longitude has to fulfill
def check_longitude(longitude):
    if longitude is not None:
        try:
            number = float(longitude)
            if number > 180 or number < -180:
                return False
            return True
        except ValueError:
            return False
    return False


# Validate add record form inputs : If at least one input is empty, the submit button is disabled
@app.callback(
    Output('add_record_button', 'disabled'),
    [Input('type', 'value'), Input('latitude', 'value'), Input('longitude', 'value')],
)
def add_record_input_validation(type, latitude, longitude):
    if (
        check_latitude(latitude) == False
        or check_longitude(longitude) == False
        or type is None
    ):
        return True
    return False


# Latitude input feedback : If the latitude is not valid, feedback will be shown to the user
@app.callback(
    Output('latitude', 'invalid'), Input('latitude', 'value'), prevent_initial_call=True
)
def latitude_validation(latitude):
    if check_latitude(latitude) == False:
        return True
    return False


# Longitude input feedback : If the longitude is not valid, feedback will be shown to the user
@app.callback(
    Output('longitude', 'invalid'),
    Input('longitude', 'value'),
    prevent_initial_call=True,
)
def longitude_validation(longitude):
    if check_longitude(longitude) == False:
        return True
    return False


# Filter records modal :  Allows the user to open the modal to filter the records
@app.callback(
    Output('filter_records_modal', 'is_open', allow_duplicate=True),
    Input('open_filter_records_modal', 'n_clicks'),
    State('filter_records_modal', 'is_open'),
    prevent_initial_call=True,
)
def toggle_filter_records_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


# Show records:  Shows the records in the table by default when accesing index but also when using filters
@app.callback(
    [ Output('table', 'data'), Output('table', 'columns'), Output('filter_records_modal','is_open')],
    [
        Input('filter_records_button', 'n_clicks'),
        State('type_filter', 'value'),
        State('day_filter', 'value'),
        State('month_filter', 'value'),
        State('year_filter', 'value'),
    ],
)
def show_records(n, type_filter, day_filter, month_filter, year_filter):
    if n > 0:
        if type_filter is None:
            type_filter = ''
        if day_filter is None:
            day_filter = ''
        if month_filter is None:
            month_filter = ''
        if year_filter is None:
            year_filter = ''
        cur.execute(
            'CALL filter_records(%s,%s,%s,%s)',
            (type_filter, day_filter, month_filter, year_filter),
        )
        data = cur.fetchall()
        dataa,columns=create_table(data)
        return dataa,columns, False
    cur.execute('CALL obtain_records()')
    data = cur.fetchall()
    dataa,columns=create_table(data)
    return dataa,columns, False



# Add record form : Inserts the given information as a record in the db and shows succesful alert
@app.callback(
    [
        Output('added_record_alert', 'is_open'),
        Output('add_record_modal', 'is_open', allow_duplicate=True),
    ],
    Input('add_record_button', 'n_clicks'),
    [State('type', 'value'), State('latitude', 'value'), State('longitude', 'value')],
    prevent_initial_call=True,
)
def add_record(n_clicks, type, latitude, longitude):
    if n_clicks > 0:
        cur.execute(
            'CALL add_record(%s,%s,%s,%s)', (session['user'], type, latitude, longitude)
        )
        conn.commit()
        return True, False


# When record added alert is closed, refreshes the page
@app.callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input('added_record_alert', 'is_open'),
    prevent_initial_call=True,
)
def redirect_after_alert(change):
    if not change:
        time.sleep(0.1)
        return '/index'
    raise PreventUpdate


# Returns the html table of the given data
def create_table(data):
    columns = [
        {"name": "id", "id": "id"},
        {"name": "Tipo", "id": "type"},
        {"name": "Ubicación", "id": "location"},
        {"name": "Fecha de admisión", "id": "time"},
        {"name": "Registrado por", "id": "added_by"},
        {"name": "Eliminar", "id": "delete", "presentation": "markdown"}

    ]
    result = []
    for row in data:
        row_dict = dict(zip([desc[0] for desc in cur.description], row))
        result.append({
            "id": row_dict["id"],
            "type":row_dict['type'],
            "location": row_dict["location"],
            "time":row_dict["time"],
            "added_by": row_dict["added_by"],
            "delete": f"[X](delete_record/{row_dict['id']})"

        })
    return result, columns


# Sign out :  When user clicks 'close session', the session variable is popped and the user is redirected to login
@app.callback(
    Output('url', 'pathname'),
    Input('sign_out_button', 'n_clicks'),
    prevent_initial_call=True,
)
def sign_out(clicked):
    if clicked:
        session.pop('user', None)
        return '/login'
    raise PreventUpdate
    
#PASSWORD RECOVERY

#Validate email form input : If the input is empty, the submit button is disabled
@app.callback(
    Output('password_recovery_submit_button', 'disabled'),
    Input('recovery_email', 'value'))

def password_recovery_input_validation(email):
        if email is None or check_email(email):
            return True
        return False

#Recovery email input feedback : If the email is not valid, feedback will be shown to the user
@app.callback(
    Output('recovery_email', 'invalid'),
    Input('recovery_email', 'value'),
    prevent_initial_call=True
)

def show_password_recovery_email_feedback(email):
    if check_email(email):
        return True
    return False

# Password recovery send mail: When the send email button is clicked, if the email exists in the db, it will create a token and send the recovery link
@app.callback(
    [Output('password_recovery_form', 'children'), Output('sent_mail_alert', 'is_open')],
    Input('password_recovery_submit_button', 'n_clicks'),
    State('recovery_email', 'value'),
    prevent_initial_call=True,
)
def send_recovery_mail(n_clicks, email):
    if n_clicks is not None:
        cur.execute('CALL user_exist(%s)', (email,))
        data= cur.fetchone()
        if data[0]!=0:
            token=get_token(data[1])
            msg = Message("Cambio de contraseña - Kanan", recipients=[data[0]], sender=("Kanan", "territoriamtyy@gmail.com"))
            msg.body = f"""Hola {email},\n\n
                        Para cambiar tu contraseña, por favor da click en el siguiente enlace:\n
                        {url_for('restore_password',token=token,_external=True)}\n
                        El enlace vencerá después de 10 minutos.\n
                        Si no solicitaste un cambio de contraseña, por favor ignora este mensaje.\n\n
                        Saludos
                        """
            mail.send(msg)
            return True,True
        return True,True
    return True,False

if __name__ == '__main__':
    app.run_server(debug=True)

conn.close()
