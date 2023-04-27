import dash
import pandas as pd
from dash import Dash, dash_table, html, dcc, Input, Output
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/index")

# Add record form inputs
type_input = html.Div(
    [
        dbc.Label("Tipo", html_for="type", className="form_label"),
        dcc.Dropdown(
            id="type",
            placeholder="Selecciona un tipo",
            options=[
                {"label": "Criminalidad", "value": "criminalidad"},
                {"label": "Seguridad", "value": "seguridad"},
            ],
            className="form_field_record",
            style={'height': 40, 'fontSize': 16}
        ),
    ],
    className="mb-3"
)

latitude_input = html.Div(
    [
        dbc.Input(
            type="text",
            id="latitude",
            placeholder="Ingresa la latitud",
            className="form_field_record",
            maxLength=19,
            style={'height': 40, 'fontSize': 16}
        ),
        # Alert
        dbc.FormFeedback("Ingresa una latitud válida.", type="invalid")
    ],
    className="mb-3"
)

longitude_input = html.Div(
    [
        dbc.Input(
            type="text",
            id="longitude",
            placeholder="Ingresa la longitud",
            className="form_field_record",
            maxLength=19,
            style={'height': 40, 'fontSize': 16}
        ),
        # Alert
        dbc.FormFeedback("Ingresa una longitud válida.", type="invalid")
    ],
    className="mb-3"
)

# Filter records inputs
type_filter_input = html.Div(
    [
        dbc.Label("Tipo", html_for="type_filter", className="form_label"),

        dcc.Dropdown(
            id="type_filter",
            placeholder="Cualquiera",
            options=[
                {"label": "Criminalidad", "value": "criminalidad"},
                {"label": "Seguridad", "value": "seguridad"},
            ],
            className="form_field_record",
            style={'height': 40, 'fontSize': 16}
        ),
    ],
    className="mb-3"
)

day_options = [{'label': str(day), 'value': day} for day in range(1, 32)]

day_filter_input = html.Div(
    [
        dcc.Dropdown(
            id="day_filter",
            placeholder="Día",
            options=day_options,
            className="form_field_record",
            style={'height': 40, 'fontSize': 16}
        ),
    ],
    className="mb-3"
)

month_filter_input = html.Div(
    [
        dcc.Dropdown(
            id="month_filter",
            placeholder="Mes",
            options=[
                {"label": "Enero", "value": "1"},
                {"label": "Febrero", "value": "2"},
                {"label": "Marzo", "value": "3"},
                {"label": "Abril", "value": "4"},
                {"label": "Mayo", "value": "5"},
                {"label": "Junio", "value": "6"},
                {"label": "Julio", "value": "7"},
                {"label": "Agosto", "value": "8"},
                {"label": "Septiembre", "value": "9"},
                {"label": "Octubre", "value": "10"},
                {"label": "Noviembre", "value": "11"},
                {"label": "Diciembre", "value": "12"},
            ],
            className="form_field_record",
            style={"height": 40, "fontSize": 16}
        ),
    ],
    className="mb-3"
)

year_filter_input = html.Div(
    [
        dcc.Dropdown(
            id="year_filter",
            placeholder="Año",
            options=[
                {"label": "2020", "value": "2020"},
                {"label": "2021", "value": "2021"},
                {"label": "2022", "value": "2022"},
                {"label": "2023", "value": "2023"},
                {"label": "2024", "value": "2024"},
            ],
            className="form_field_record",
            style={"height": 40, "fontSize": 16}
        ),
    ],
    className="mb-3"
)

# Page layout
layout = dbc.Container([
    
    # Heading
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
                    dbc.NavItem(dbc.NavLink("Cerrar sesión", href="/login", id="sign_out_button", n_clicks=0)),
                    dbc.NavItem(dbc.NavLink("Territoria", href="/territoria")),
                    dbc.NavItem(dbc.NavLink("Sección Violeta", href="/seccionvioleta"))
                ], className="ms-auto", navbar=True),
                id="navbar-collapse", navbar=True,
            )       
        ]), color="#FFFFFF", dark=False, className="head_margin"
    ),

    # Record added successfully alert
    html.Div(
        dbc.Alert(
            "El reporte fue agregado con éxito.",
            color="success", 
            id="added_record_alert",
            is_open=False,
            duration=7000
        )
    ),

    # Add record modal
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Agregar registro")),

            dbc.ModalBody(
                html.Div(
                    # Add record form
                    dbc.Form(
                        html.Div(
                            [  
                                dbc.Row(dbc.Col(type_input)),
                                dbc.Row(dbc.Col(html.Label("Ubicación", className="form_label margin_7"))),
                                dbc.Row(
                                    [
                                        dbc.Col(latitude_input),
                                        dbc.Col(longitude_input)
                                    ]
                                )
                            ]
                        )
                    ),
                    id="add_record_form"
                )
            ),

            dbc.ModalFooter(dbc.Button("Agregar", id="add_record_button", className="ms-auto submit_btn", n_clicks=0)), 
        ],

        id="add_record_modal", is_open=False
    ),

    # Filter table records modal
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Filtrar registros")),
            dbc.ModalBody(
                html.Div(
                    # Filter records form
                    dbc.Form(
                        [
                            dbc.Row(type_filter_input),
                            dbc.Row(dbc.Col(html.Label('Fecha', className='form_label margin_7'))),
                            dbc.Row(
                                [
                                    dbc.Col(day_filter_input),
                                    dbc.Col(month_filter_input),
                                    dbc.Col(year_filter_input)
                                ]
                            )
                        ]
                    ),
                    id="filter_records_form"
                )
            ),
            dbc.ModalFooter(dbc.Button("Filtrar", id="filter_records_button", className="ms-auto submit_btn", n_clicks=0)),
        ],
        id="filter_records_modal",
        is_open=False
    ),


    # Main div
    html.Div(
        [
            # Title
            html.H1("Registros", className="title"),

            html.Div(
                [
                    # Add record button
                    dbc.Button(
                        html.Span(
                            [
                                html.I(className="fas fa-plus"),
                                " Agregar"
                            ]
                        ),
                        id="open_add_record_modal",
                        n_clicks=0,
                        className="me-2 submit_btn margin_bottom_20"
                    ),

                    # Filter table records button
                    dbc.Button(
                        html.Span(
                            [
                                html.I(className="fas fa-filter"),
                                "  Filtrar"
                            ]
                        ),
                        id="open_filter_records_modal",
                        n_clicks=0,
                        className="submit_btn margin_bottom_20"
                    )
                ],
                className="index_buttons_div"
            ),

        ],
        className="index_div"
    ),

    # Security records table
    html.Div(id='table', className="table"),
    html.Br(),
    html.Br(),
    html.Br(),
], fluid=False)
