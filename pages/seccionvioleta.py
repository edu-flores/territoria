import dash
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/seccionvioleta")


# Page layout

layout = dbc.Container([

    dbc.Navbar(
        dbc.Container([

            html.A(
                dbc.Row(
                    dbc.Col(html.Img(src="assets/georregias_logo.jpeg", height="30px")),
                    align="center", className="g-0"
                ), href="/"
            ),

            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),

            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("Territoria", href="/territoria")),
                    dbc.NavItem(dbc.NavLink("Sección Violeta", href="/seccionvioleta"))
                ], className="ms-auto", navbar=True),
                id="navbar-collapse", navbar=True,
            )

        ]), color="#FFFFFF", dark=False,
    ),

    dbc.Row(
        dbc.Col(html.Img(src="assets/seccionvioleta_banner.jpg", className="img-fluid")),
        className="pt-1", justify="center"
    ),

    dbc.Row([
        dbc.Col([
            html.P([
                "La Sección Violeta es una",
                html.Strong(" guía gratuita, práctica, accesible e inclusiva para mujeres de todos los"
                            " contextos"),
                " que se encuentren en situaciones de vulnerabilidad para que, en caso de una emergencia o"
                " situación de riesgo, conozcan las asociaciones, instituciones y colectivos a quienes pueden"
                " recurrir."
            ]),
            html.P([
                "Para leer la Sección Violeta haz ",
                html.A(" click aquí", href="https://commons.wikimedia.org/wiki/File:Secci%C3%B3n_Violeta.pdf",
                       style={"color": "#A777B1"}, target="_blank")
            ])
            ,
        ], style={"fontSize": "22px"}, lg=11
        )

    ], class_name="pt-4 pb-5", justify="center"
    ),

    dbc.Row([
        dbc.Col(
            html.B("¿Quieres ayudarnos a generar espacios seguros para todas y todes?")
        , style={"fontSize": "20px"}, lg=11
        )
    ], class_name="pt-4 pb-2", justify="center", style={"backgroundColor":"#F6F8FA", "textAlign": "center"}
    ),

    dbc.Row([
        dbc.Col([
            html.P(
                "Envíanos un mensaje o correo y platiquemos 💜"
            , style={"fontSize": "18px"}
            ),
            html.P([
                "Instagram: ",
                html.A(" georregias", href="https://www.instagram.com/georregias", style={"color": "#A777B1"},
                       target="_blank")
            ], style={"fontSize": "16px"}
            ),
            html.P([
                "Facebook: ",
                html.A(" Georregias", href="https://www.facebook.com/Georregias", style={"color": "#A777B1"},
                       target="_blank")
            ], style={"fontSize": "16px"}
            ),
            html.P(
                "Correo: georregias@gmail.com"
                , style={"fontSize": "16px"}
            )
        ], lg=11
        )

    ], class_name="pt-2 pb-3", justify="center", style={"backgroundColor":"#F6F8FA", "textAlign": "center"}
    ),




], fluid=False)