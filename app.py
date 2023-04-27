import dash
from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.graph_objects as go
import os
import mariadb

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

app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-57PKT06DTW"></script>
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
</html>"""

server = app.server


# Page layout
app.layout = html.Div([

    dash.page_container

])


# Navbar - Callback
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)(toggle_navbar_collapse)


# Sidebar - Callback
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)(toggle_offcanvas)


# Map

# Access token
token = "pk.eyJ1IjoianB6cDIwMDEiLCJhIjoiY2xmcmEzNnhyMDNjdDNycXQ0d3A2N3NjbyJ9.PUJ_q_U96vOQ94oli7JT6g"

# Map layout
map_layout = dict(
    mapbox={
        'accesstoken': token,
        'style': "light",
        'zoom': 13,
        'center': dict(lat=25.675456439828732, lon=-100.31115409182688)
    },
    showlegend=False,
    margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
    modebar=dict(remove=["zoom", "toimage", "pan", "select", "lasso", "zoomin", "zoomout", "autoscale", "reset",
                         "resetscale", "resetview"]),
    hoverlabel_bgcolor="#000000"
)

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root", password="root", host="localhost", port=3307, database="georregias"
    )
    cur = conn.cursor()
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")

# Estaciones de Metro
estaciones_metro = pd.read_csv("assets/estaciones_metro.csv")

# Reportes
cur.execute("SELECT SUBSTRING_INDEX(location,',', 1) AS lat, SUBSTR(location, POSITION(',' IN  location)+2, LENGTH(location)) AS lon FROM record WHERE type='911';")
reportes = cur.fetchall()

# Percepciones - Espacio inseguro y de peligro
cur.execute("SELECT SUBSTRING_INDEX(location,',', 1) AS lat, SUBSTR(location, POSITION(',' IN  location)+2, LENGTH(location)) AS lon FROM record WHERE type='criminalidad';")
percepciones = cur.fetchall()

# Percepciones - Espacio seguro
cur.execute("SELECT SUBSTRING_INDEX(location,',', 1) AS lat, SUBSTR(location, POSITION(',' IN  location)+2, LENGTH(location)) AS lon FROM record WHERE type='seguridad';")
percepciones_seguro = cur.fetchall()

# Map - Callback
def on_form_change(switches_value):

    #print(switches_value)
    #print(len(switches_value))

    if switches_value == [1]:
        #print("passed through (1)")

        estaciones_mapa = go.Figure(go.Scattermapbox(
            lon=estaciones_metro["longitud"],
            lat=estaciones_metro["latitud"],
            marker={'size': 14, 'symbol': "rail-metro", "opacity": 1},
            hovertext=estaciones_metro["name"],
            hoverinfo="text"
        ))

        estaciones_mapa.update_layout(map_layout)

        return estaciones_mapa

    elif switches_value == [2]:
       #print("passed through (2)")

        reportes_mapa = go.Figure(go.Scattermapbox(
            lon=list(map(lambda x: x[0], reportes)),
            lat=list(map(lambda x: x[1], reportes)),
            marker={'size': 0, 'opacity': .1, 'color': '#4974a5'},
            cluster={
                'enabled': True,
                'size': [12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 69, 78],
                "step": [60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 720, 780, 840, 900, 960, 1020, 2100,
                         5200],
                # "step": [50, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3500,
                #          4000, 4500, 5000],
                'color': '#4974a5',
                'opacity': .3
            }
        ))

        reportes_mapa.update_layout(map_layout)

        return reportes_mapa

    elif switches_value == [3]:
        #print("passed through (3)")

        percepciones_mapa = go.Figure(go.Scattermapbox(
            lon=list(map(lambda x: x[0], percepciones)),
            lat=list(map(lambda x: x[1], percepciones)),
            marker={'size': 14, 'opacity': .7, 'color': '#A97BB5'},
            hoverinfo="none"
        ))

        percepciones_mapa.update_layout(map_layout)

        return percepciones_mapa

    elif switches_value == [4]:
        #print("passed through (4)")

        percepciones_seguro_mapa = go.Figure(go.Scattermapbox(
            lon=list(map(lambda x: x[0], percepciones_seguro)),
            lat=list(map(lambda x: x[1], percepciones_seguro)),
            marker={'size': 14, 'opacity': .7, 'color': '#8bb77f'},
            hoverinfo="none"
        ))

        percepciones_seguro_mapa.update_layout(map_layout)

        return percepciones_seguro_mapa

    elif switches_value == [1, 2] or switches_value == [2, 1]:
        #print("passed through (1, 2)")

        # Estaciones + Reportes
        estaciones_reportes = go.Figure(go.Scattermapbox(
            lon=list(map(lambda x: x[0], reportes)),
            lat=list(map(lambda x: x[1], reportes)),
            marker={'size': 0, 'opacity': .1, 'color': '#4974a5'},
            cluster={
                'enabled': True,
                'size': [12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 69, 78],
                "step": [60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 720, 780, 840, 900, 960, 1020, 2100,
                         5200],
                'color': '#4974a5',
                'opacity': .3
            }
        ))

        estaciones_reportes.add_scattermapbox(
            lon=estaciones_metro["longitud"],
            lat=estaciones_metro["latitud"],
            marker={'size': 14, 'symbol': "rail-metro", "opacity": 1},
            hovertext=estaciones_metro["name"],
            hoverinfo="text"
        )

        estaciones_reportes.update_layout(map_layout)

        return estaciones_reportes

    elif switches_value == [1, 3] or switches_value == [3, 1]:
        #print("passed through (1, 3)")

        # Estaciones + Percepciones
        estaciones_percepciones = go.Figure(go.Scattermapbox(
            lon=list(map(lambda x: x[0], percepciones)),
            lat=list(map(lambda x: x[1], percepciones)),
            marker={'size': 14, 'opacity': .7, 'color': '#A97BB5'},
            hoverinfo="none"
        ))

        estaciones_percepciones.add_scattermapbox(
            lon=estaciones_metro["longitud"],
            lat=estaciones_metro["latitud"],
            marker={'size': 14, 'symbol': "rail-metro", "opacity": 1},
            hovertext=estaciones_metro["name"],
            hoverinfo="text"
        )

        estaciones_percepciones.update_layout(map_layout)

        return estaciones_percepciones

    elif switches_value == [1, 4] or switches_value == [4, 1]:
        #print("passed through (1, 4)")

        # Estaciones + Percepciones - Seguro
        estaciones_percepciones_seguro = go.Figure(go.Scattermapbox(
            lon=list(map(lambda x: x[0], percepciones_seguro)),
            lat=list(map(lambda x: x[1], percepciones_seguro)),
            marker={'size': 14, 'opacity': .7, 'color': '#8bb77f'},
            hoverinfo="none"
        ))

        estaciones_percepciones_seguro.add_scattermapbox(
            lon=estaciones_metro["longitud"],
            lat=estaciones_metro["latitud"],
            marker={'size': 14, 'symbol': "rail-metro", "opacity": 1},
            hovertext=estaciones_metro["name"],
            hoverinfo="text"
        )

        estaciones_percepciones_seguro.update_layout(map_layout)

        return estaciones_percepciones_seguro

    elif switches_value == [2, 3] or switches_value == [3, 2]:
        #print("passed through (2, 3)")

        # Reportes + Percepciones
        reportes_percepciones = go.Figure(go.Scattermapbox(
            lon=list(map(lambda x: x[0], reportes)),
            lat=list(map(lambda x: x[1], reportes)),
            marker={'size': 0, 'opacity': .1, 'color': '#4974a5'},
            cluster={
                'enabled': True,
                'size': [12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 69, 78],
                "step": [60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 720, 780, 840, 900, 960, 1020, 2100,
                         5200],
                'color': '#4974a5',
                'opacity': .3
            }
        ))

        reportes_percepciones.add_scattermapbox(
            lon=list(map(lambda x: x[0], percepciones)),
            lat=list(map(lambda x: x[1], percepciones)),
            marker = {'size': 14, 'opacity': .7, 'color': '#A97BB5'},
            hoverinfo = "none"
        )

        reportes_percepciones.update_layout(map_layout)

        return reportes_percepciones

    elif switches_value == [2, 4] or switches_value == [4, 2]:
        #print("passed through (2-4)")

        # Reportes + Percepciones - Seguro
        reportes_percepciones_seguro = go.Figure(go.Scattermapbox(
            lon=list(map(lambda x: x[0], reportes)),
            lat=list(map(lambda x: x[1], reportes)),
            marker = {'size': 0, 'opacity': .1, 'color': '#4974a5'},
            cluster = {
                'enabled': True,
                'size': [12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 69, 78],
                "step": [60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 720, 780, 840, 900, 960, 1020, 2100,
                         5200],
                'color': '#4974a5',
                'opacity': .3
            }
        ))

        reportes_percepciones_seguro.add_scattermapbox(
            lon=list(map(lambda x: x[0], percepciones_seguro)),
            lat=list(map(lambda x: x[1], percepciones_seguro)),
            marker={'size': 14, 'opacity': .7, 'color': '#8bb77f'},
            hoverinfo="none"
        )

        reportes_percepciones_seguro.update_layout(map_layout)

        return reportes_percepciones_seguro

    elif switches_value == [3, 4] or switches_value == [4, 3]:
        #print("passed through (3-4)")

        # Ambas Percepciones
        percepciones_ambas = go.Figure(go.Scattermapbox(
            lon=list(map(lambda x: x[0], percepciones_seguro)),
            lat=list(map(lambda x: x[1], percepciones_seguro)),
            marker={'size': 14, 'opacity': .7, 'color': '#8bb77f'},
            hoverinfo="none"
        ))

        percepciones_ambas.add_scattermapbox(
            lon=list(map(lambda x: x[0], percepciones)),
            lat=list(map(lambda x: x[1], percepciones)),
            marker={'size': 14, 'opacity': .7, 'color': '#A97BB5'},
            hoverinfo="none"
        )

        percepciones_ambas.update_layout(map_layout)

        return percepciones_ambas

    elif switches_value == [1, 2, 3] or switches_value == [1, 3, 2] or switches_value == [2, 1, 3]\
            or switches_value == [2, 3, 1] or switches_value == [3, 1, 2] or switches_value == [3, 2, 1]:
        #print("passed through (1, 2, 3)")

        # Estaciones + Reportes + Percepciones
        estaciones_reportes_percepciones = go.Figure(go.Scattermapbox(
            lon=list(map(lambda x: x[0], reportes)),
            lat=list(map(lambda x: x[1], reportes)),
            marker={'size': 0, 'opacity': .1, 'color': '#4974a5'},
            cluster={
                'enabled': True,
                'size': [12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 69, 78],
                "step": [60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 720, 780, 840, 900, 960, 1020, 2100,
                         5200],
                'color': '#4974a5',
                'opacity': .3
            }
        ))

        estaciones_reportes_percepciones.add_scattermapbox(
            lon=list(map(lambda x: x[0], percepciones)),
            lat=list(map(lambda x: x[1], percepciones)),
            marker={'size': 14, 'opacity': .7, 'color': '#A97BB5'},
            hoverinfo="none"
        )

        estaciones_reportes_percepciones.add_scattermapbox(
            lon=estaciones_metro["longitud"],
            lat=estaciones_metro["latitud"],
            marker={'size': 14, 'symbol': "rail-metro", "opacity": 1},
            hovertext=estaciones_metro["name"],
            hoverinfo="text"
        )

        estaciones_reportes_percepciones.update_layout(map_layout)

        return estaciones_reportes_percepciones

    elif switches_value == [1, 2, 4] or switches_value == [1, 4, 2] or switches_value == [2, 1, 4]\
            or switches_value == [2, 4, 1] or switches_value == [4, 1, 2] or switches_value == [4, 2, 1]:
        #print("passed through (1, 2, 4)")

        # Estaciones + Reportes + Percepciones - Seguro
        estaciones_reportes_percepciones_seguro = go.Figure(go.Scattermapbox(
            lon=list(map(lambda x: x[0], reportes)),
            lat=list(map(lambda x: x[1], reportes)),
            marker={'size': 0, 'opacity': .1, 'color': '#4974a5'},
            cluster={
                'enabled': True,
                'size': [12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 69, 78],
                "step": [60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 720, 780, 840, 900, 960, 1020, 2100,
                         5200],
                'color': '#4974a5',
                'opacity': .3
            }
        ))

        estaciones_reportes_percepciones_seguro.add_scattermapbox(
            lon=list(map(lambda x: x[0], percepciones_seguro)),
            lat=list(map(lambda x: x[1], percepciones_seguro)),
            marker={'size': 14, 'opacity': .7, 'color': '#8bb77f'},
            hoverinfo="none"
        )

        estaciones_reportes_percepciones_seguro.add_scattermapbox(
            lon=estaciones_metro["longitud"],
            lat=estaciones_metro["latitud"],
            marker={'size': 14, 'symbol': "rail-metro", "opacity": 1},
            hovertext=estaciones_metro["name"],
            hoverinfo="text"
        )

        estaciones_reportes_percepciones_seguro.update_layout(map_layout)

        return estaciones_reportes_percepciones_seguro


    elif switches_value == [1, 3, 4] or switches_value == [1, 4, 3] or switches_value == [3, 1, 4] \
            or switches_value == [3, 4, 1] or switches_value == [4, 1, 3] or switches_value == [4, 3, 1]:
        #print("passed through (1, 3, 4)")

        # Estaciones + Ambas Percepciones
        estaciones_percepciones_ambas = go.Figure(go.Scattermapbox(
            lon=list(map(lambda x: x[0], percepciones_seguro)),
            lat=list(map(lambda x: x[1], percepciones_seguro)),
            marker={'size': 14, 'opacity': .7, 'color': '#8bb77f'},
            hoverinfo="none"
        ))

        estaciones_percepciones_ambas.add_scattermapbox(
            lon=list(map(lambda x: x[0], percepciones)),
            lat=list(map(lambda x: x[1], percepciones)),
            marker={'size': 14, 'opacity': .7, 'color': '#A97BB5'},
            hoverinfo="none"
        )

        estaciones_percepciones_ambas.add_scattermapbox(
            lon=estaciones_metro["longitud"],
            lat=estaciones_metro["latitud"],
            marker={'size': 14, 'symbol': "rail-metro", "opacity": 1},
            hovertext=estaciones_metro["name"],
            hoverinfo="text"
        )

        estaciones_percepciones_ambas.update_layout(map_layout)

        return estaciones_percepciones_ambas

    elif switches_value == [2, 3, 4] or switches_value == [2, 4, 3] or switches_value == [3, 2, 4]\
            or switches_value == [3, 4, 2] or switches_value == [4, 2, 3] or switches_value == [4, 3, 2]:
        #print("passed through (2, 3, 4)")

        # Reportes + Ambas Percepciones
        reportes_percepciones_ambas = go.Figure(go.Scattermapbox(
            lon=list(map(lambda x: x[0], reportes)),
            lat=list(map(lambda x: x[1], reportes)),
            marker={'size': 0, 'opacity': .1, 'color': '#4974a5'},
            cluster={
                'enabled': True,
                'size': [12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 69, 78],
                "step": [60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 720, 780, 840, 900, 960, 1020, 2100,
                         5200],
                'color': '#4974a5',
                'opacity': .3
            }
        ))

        reportes_percepciones_ambas.add_scattermapbox(
            lon=list(map(lambda x: x[0], percepciones_seguro)),
            lat=list(map(lambda x: x[1], percepciones_seguro)),
            marker={'size': 14, 'opacity': .7, 'color': '#8bb77f'},
            hoverinfo="none"
        )

        reportes_percepciones_ambas.add_scattermapbox(
            lon=list(map(lambda x: x[0], percepciones)),
            lat=list(map(lambda x: x[1], percepciones)),
            marker={'size': 14, 'opacity': .7, 'color': '#A97BB5'},
            hoverinfo="none"
        )

        reportes_percepciones_ambas.update_layout(map_layout)

        return reportes_percepciones_ambas

    elif len(switches_value) == 4:
        #print("passed though todas")

        # Mapa - Todas
        mapa_todas = go.Figure(go.Scattermapbox(
            lon=list(map(lambda x: x[0], reportes)),
            lat=list(map(lambda x: x[1], reportes)),
            marker={'size': 0, 'opacity': .1, 'color': '#4974a5'},
            cluster={
                'enabled': True,
                'size': [12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 69, 78],
                "step": [60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 720, 780, 840, 900, 960, 1020, 2100,
                         5200],
                'color': '#4974a5',
                'opacity': .3
            }
        ))

        mapa_todas.add_scattermapbox(
            lon=list(map(lambda x: x[0], percepciones_seguro)),
            lat=list(map(lambda x: x[1], percepciones_seguro)),
            marker={'size': 14, 'opacity': .7, 'color': '#8bb77f'},
            hoverinfo="none"
        )

        mapa_todas.add_scattermapbox(
            lon=list(map(lambda x: x[0], percepciones)),
            lat=list(map(lambda x: x[1], percepciones)),
            marker={'size': 14, 'opacity': .7, 'color': '#A97BB5'},
            hoverinfo="none"
        )

        mapa_todas.add_scattermapbox(
            lon=estaciones_metro["longitud"],
            lat=estaciones_metro["latitud"],
            marker={'size': 14, 'symbol': "rail-metro", "opacity": 1},
            hovertext=estaciones_metro["name"],
            hoverinfo="text"
        )

        mapa_todas.update_layout(map_layout)

        return mapa_todas

    elif len(switches_value) == 0:
        #print("passed through (0)")

        placeholder = go.Figure(go.Scattermapbox(
            lon=list(map(lambda x: x[0], percepciones)),
            lat=list(map(lambda x: x[1], percepciones)),
            marker={'size': 0, 'opacity': .5, 'color': '#E2474B'},
            hoverinfo="none"
        ))

        placeholder.update_layout(map_layout)

        return placeholder

app.callback(
    Output("mapa-movil", "figure"),
    Input("switches-input-movil", "value")
)(on_form_change)

app.callback(
    Output("mapa-desktop", "figure"),
    Input("switches-input-desktop", "value")
)(on_form_change)

if __name__ == '__main__':
    app.run_server(debug=True)

conn.close()
