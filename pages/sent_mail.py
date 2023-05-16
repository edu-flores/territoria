
import dash
from dash import Dash, html,Input,Output,dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/sent_mail')

# Page layout
layout = dbc.Container([

    #Heading
    dbc.Navbar(
        dbc.Container([

            html.A(
                dbc.Row(
                    dbc.Col(html.Img(src='assets/logo.jpeg', height='30px')),
                    align='center', className='g-0'
                ), href='/'
            ),

            dbc.NavbarToggler(id='navbar-toggler', n_clicks=0),


            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink('Iniciar Sesión', href='/login')),
                ], className='ms-auto', navbar=True),
                id='navbar-collapse', navbar=True,
            )
            
        ]), color='#FFFFFF', dark=False,  className='head_margin'
    ),
    
    #Icono
    html.Div(
        [
             html.I(className='bi bi-check-circle', style={'fontSize':150, 'color':'#8D65C5'})
        ], style={'textAlign':'center', 'marginLeft':'auto', 'marginRight':'auto', 'marginTop':30 }
    ),
    

    #Title
    html.H1('Correo de recuperación enviado', style={'textAlign': 'center', 'fontSize':40, 'marginBottom':20, 'marginTop':15}),

    #Legend
    html.P('Te hemos enviado un correo con instrucciones para restablecer tu contraseña.', style={'textAlign': 'center', 'width':'45%', 'marginLeft':'auto', 'marginRight':'auto', 'marginTop':15, 'fontSize':18}),

    #Sent button
    html.Div([
             html.Div(
                [
                    dbc.Button(
                        'Reenviar email', id='submitBtn', className='me-2', style={'backgroundColor': '#8D65C5', 'border': '1px solid #8D65C5', 'fontWeight': 600, 'fontSize':16, 'height': 50, 'margin-top':30,}, 
                    ),
                ], style={'textAlign':'center'}
             )
             
    ] ,style={'margin':'auto', 'width':'55%'} )

], fluid=False)

   
