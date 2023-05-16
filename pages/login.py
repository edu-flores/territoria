import dash
from dash import Dash, html,Input,Output,dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/login')

#Login form inputs
email_input = html.Div(
    [
        dbc.Label('Email', html_for='email', className='form_label'),
        dbc.Input(type='text',
                  id='email', 
                  placeholder='Ingresa tu correo electrónico',
                  className='form_field_login',
                  maxLength=100,autocomplete=False),
        #Alert
         dbc.FormFeedback('Ingrese un correo electrónico válido.',
                          type='invalid',
        ),
    ],
    className='mb-3'
)

password_input = html.Div(
    [
        dbc.Label('Password', html_for='password', className='form_label'),
        dbc.Input(
            type='password',
            id='password',
            placeholder='Ingresa tu contraseña',
            className='form_field_login',
            maxLength=50),
        #Alert
         dbc.FormFeedback('Ingrese una contraseña válida.',
                          type='invalid',
        )
    ],
    className='mb-3',
)


# Page layout
layout = dbc.Container([

    #Heading
    dbc.Navbar(
        dbc.Container([

            html.A(
                dbc.Row(
                    dbc.Col(html.Img(src='assets/logo.jpeg', height='30px')),
                    align='center', className='g-0 nav_margin_top'
                ), href='/'
            ),

            dbc.NavbarToggler(id='navbar-toggler', n_clicks=0),

            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink('Mapa', href='/'))
                ], className='ms-auto', navbar=True),
                id='navbar-collapse', navbar=True,
            )

        ]), color='#FFFFFF', dark=False, className='head_margin'
    ),
    

    #Alert 
    html.Div(dbc.Alert('Las credenciales son incorrectas. Vuelva a intentarlo.', color='danger', id='bad_credentials_alert',className='bad_c_alert',is_open=False, duration=5000)),

    

    #Main div
    html.Div([
    
            #Title
            html.H1('Iniciar sesión',className='title'),

            #Login Form
             dbc.Form([email_input, password_input]),

             html.Div(
                [
                    dbc.Button(
                        'Iniciar sesión', id='submit_button',type='submit', className='me-2 submit_btn btn_margin', 
                    ),
                ], className='text_center'
             ),

             html.Div(id='login_form'),

            #Password recovery link
            html.Div(
                  [
                    html.A('¿Olvidaste tu contraseña?', href='/password_recovery', className='password_recovery_link'),
                  ], className='password_recovery_div'),

          
    ],className='login_form_div'),

     
    
 
], fluid=False)

   
