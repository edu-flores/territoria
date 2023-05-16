import dash
from dash import Dash, html,Input,Output,dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/password_recovery')

#Password recovery form inputs
email_input = html.Div(
    [
        dbc.Label('Email', html_for='recovery_email', className='form_label'),
        dbc.Input(type='email',
                  id='recovery_email', 
                  placeholder='Ingresa tu correo electrónico',
                  className='mb-3 form_field_password_recovery'),   
        #Alert
        dbc.FormFeedback('Ingrese un correo electrónico válido.',
                          type='invalid',
        ),
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
                    dbc.Col(html.Img(src='assets/logo.png', height='30px')),
                    align='center', className='g-0'
                ), href='/'
            ),

            dbc.NavbarToggler(id='navbar-toggler', n_clicks=0),


            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink('Iniciar sesión', href='/login')),
                ], className='ms-auto', navbar=True),
                id='navbar-collapse', navbar=True,
            )
            
        ]), color='#FFFFFF', dark=False, className='head_margin'
    ),

    #Alert 
    html.Div(dbc.Alert('Te hemos enviado un correo con instrucciones para restablecer tu contraseña.', color='success', id='sent_mail_alert',className='sent_mail_alert',is_open=False, duration=5000)),

    #Main Div
    html.Div([
    
            #Title
            html.H1('Restablecer contraseña', className='title'),

            #Legend
            html.P('Ingresa en el formulario tu correo de administrador.',className='password_recovery_legend'),
            html.P('Te enviaremos instrucciones para restablecer la contraseña.', className='password_recovery_legend margin_bottom_20'),


            dbc.Form([email_input]),
            html.Div(id='password_recovery_form'),

             html.Div(
                [
                    dbc.Button(
                        'Enviar email', id='password_recovery_submit_button', className='me-2 submit_btn btn_margin',
                    ),
                ], className='center'
             )
             
    ] , className='password_recovery_page_div')

], fluid=False)

   
