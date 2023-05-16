import dash
from dash import Dash, html,Input,Output,dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/page_not_found')


#Page layout
layout = dbc.Container([

    # Navbar
    dbc.Navbar(
        dbc.Container([

            html.A(
                dbc.Row(
                    dbc.Col(html.Img(src='assets/logo.png', height='30px')),
                    align='center', className='g-0'
                ),
                href='/'
            ),

            dbc.NavbarToggler(id='navbar-toggler', n_clicks=0),

            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink('Mapa', href='/')),
                ], className='ms-auto', navbar=True),
                id='navbar-collapse', navbar=True,
            ),

        ]), color='#FFFFFF', dark=False, className='head_margin'
    ),

    #Title
    html.H1('Lo sentimos.', className='center title title_404'),

    #Notice
    html.Div(
                [
                    html.H3('Parece que la página que estás buscando no existe.', className='center notice'),
                   
                    #Return to home link
                    html.A('Volver a inicio', href='/', className='home_link center')

                ]
    
    ,className='div_404')
    

],fluid=False)

