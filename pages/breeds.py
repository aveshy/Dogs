import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import random

# Загрузка датасета
df = pd.read_csv('formatted_dog_breeds.csv')

# Уникальные породы собак
breeds = df['Breed'].unique()

layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H3('Особенности породы'),
                html.Hr(style={'color': '#493B32'}),
            ], style={'textAlign': 'center'})
        )
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='breed-dropdown',
                options=[{'label': breed, 'value': breed} for breed in breeds],
                placeholder="Выберите породу",
                multi=False
            )
        ], width=3)
    ]),
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Цвет шерсти'),
                     dbc.Row([
                        dbc.Col([
                            dbc.CardImg(src='/static/images/fur.png')], width= 4),
                        dbc.Col([
                            dbc.CardBody(html.P(id='fur-color', className='card-value', style={'fontSize': '20px'}),
                        )], width=8),])
                ], color='primary', outline=True, style={'textAlign': 'center', 'height': '100%'})
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Цвет глаз'),
                    dbc.Row([
                        dbc.Col([
                            dbc.CardImg(src='/static/images/eye.png')], width= 4),
                        dbc.Col([
                            dbc.CardBody(html.P(id='eye-color', className='card-value', style={'fontSize': '20px'}),
                        )], width=8),])
                ], color='primary', outline=True, style={'textAlign': 'center', 'height': '100%'})
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Продолжительность жизни'),
                    dbc.Row([
                        dbc.Col([
                            dbc.CardImg(src='/static/images/life.png')], width= 4),
                        dbc.Col([
                            dbc.CardBody(html.P(id='longevity', className='card-value', style={'fontSize': '20px'}),
                        )], width=8),])
                ], color='primary', outline=True, style={'textAlign': 'center', 'height': '100%'})
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Высота породы'),
                    dbc.Row([
                        dbc.Col([
                            dbc.CardImg(src='/static/images/height.png')], width= 4),
                        dbc.Col([
                            dbc.CardBody(html.P(id='height', className='card-value', style={'fontSize': '20px'}),
                        )], width=8),])
                ], color='primary', outline=True, style={'textAlign': 'center', 'height': '100%'})
            ], width=3)
        ])
    ]),
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Img(id='dog-image-1', className='img-fluid mb-3')
            ], md=6),
            dbc.Col([
                html.Img(id='dog-image-2', className='img-fluid mb-3')
            ], md=6)
        ])
    ])
])

@callback(
    [   Output('fur-color', 'children'),
        Output('eye-color', 'children'),
        Output('longevity', 'children'),
        Output('height', 'children'),
        Output('dog-image-1', 'src'),
        Output('dog-image-2', 'src')
    ],
    [Input('breed-dropdown', 'value')]
)
def update_breed_info(selected_breed):
    if selected_breed is None:
        return ["", "", "", "", "", ""]
   
    breed_info = df[df['Breed'] == selected_breed].iloc[0]

    fur_color = breed_info['Fur Color']
    eye_color = breed_info['Color of Eyes']
    longevity = f"min: {breed_info['Min Longevity (yrs)']} лет, max: {breed_info['Max Longevity (yrs)']} лет"
    height = f"min: {breed_info['Min Height (cm)']} см, max: {breed_info['Max Height (cm)']} см"

    image_1 = f"/static/images/{selected_breed}1.jpg"
    image_2 = f"/static/images/{selected_breed}2.jpg"

    return fur_color, eye_color, longevity, height, image_1, image_2
