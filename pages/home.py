import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")


# Page layout

layout = dbc.Container([

    # Navbar
    dbc.Navbar(
        dbc.Container([

            html.A(
                dbc.Row(
                    dbc.Col(html.Img(src="assets/georregias_logo.jpeg", height="30px")),
                    align="center", className="g-0"
                ),
                href="/"
            ),

            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),

            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("Territoria", href="/territoria")),
                    dbc.NavItem(dbc.NavLink("Sección Violeta", href="/seccionvioleta"))
                ], className="ms-auto", navbar=True),
                id="navbar-collapse", navbar=True,
            ),

        ]), color="#FFFFFF", dark=False,
    ),

    # Banner foto
    dbc.Row(
        dbc.Col(html.Img(src="assets/georregias_banner.jpg", className="img-fluid")),
        className="pt-1", justify="center"
    ),

    # Texto principal
    dbc.Row([
        dbc.Col([
            html.P([
                "Somos una colectiva enfocada en urbanismo feminista y cultura de cuidados que busca promover"
                " herramientas para que otras mujeres, de cualquier edad y origen,",
                html.Strong(" puedan habitar la ciudad y los espacios públicos de manera segura.")
            ]),
        ], style={"fontSize": "22px"}, lg=11
        )
    ],
        class_name="pt-4 pb-5",
        justify="center"
    ),

    # Footer - Title
    dbc.Row(
        dbc.Col(
            html.B("¿Quieres ayudarnos a generar espacios seguros para todas y todes?"),
            style={"fontSize": "20px"},
            lg=11
        ),
        class_name="pt-4 pb-2",
        justify="center",
        style={"backgroundColor":"#F6F8FA", "textAlign": "center"}
    ),

    # Footer - Content
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
    ],
        class_name="pt-2 pb-3",
        justify="center",
        style={"backgroundColor":"#F6F8FA", "textAlign": "center"}
    ),

],
    fluid=False
)