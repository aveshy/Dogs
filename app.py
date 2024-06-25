import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html
from pages import info, breeds, character, illnesses, facts

external_stylesheets = [dbc.themes.SKETCHY]
app = Dash(__name__, external_stylesheets=external_stylesheets,  use_pages=True)
app.config.suppress_callback_exceptions = True

# Задаем аргументы стиля для хедера
HEADER_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'width': '100%',
    'padding': '1rem',
    'background-color': '#D1BFB3',
    'z-index': 1000  # чтобы хедер всегда был поверх остальных элементов
}

# Справа от боковой панели размешается основной дашборд. Добавим отступы
CONTENT_STYLE = {
    'margin-top': '6rem',
    'margin-left': '0rem',
    'margin-right': '0rem',
    'padding': '2rem 1rem',
    'background-color': '#E4E0DD'
}

header = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(html.Img(src='/static/images/dog2.png', height='55px'), width='auto'),
                    dbc.Col(dbc.NavbarBrand('Всё о собаках', className='ms-2', style={'color': '#3B363C', 'font-size': '2rem'}), width='auto'),
                    dbc.Col(html.Br()),
                    dbc.Col(html.Br()),
                    dbc.Col(html.Br()),
                    dbc.Col(
                        dbc.Nav([
                            dbc.NavLink('Информация о проекте', href='/', active='exact', style={'color': '#7B6C63', 'text-align': 'center'}),],
                            pills=True,
                            style={'width': '100%', 'display': 'flex', 'justify-content': 'space-between'}
                            )),
                    dbc.Col(html.Br()),
                    dbc.Col(html.Br()),
                    dbc.Col(html.Br()),
                    dbc.Col(
                        dbc.Nav([
                            dbc.NavLink('Особенности породы', href='/page-1', active='exact', style={'color': '#7B6C63', 'text-align': 'center'}),],
                            pills=True,
                            style={'width': '100%', 'display': 'flex', 'justify-content': 'space-between'}
                            )),
                    dbc.Col(html.Br()),
                    dbc.Col(html.Br()),
                    dbc.Col(html.Br()),
                    dbc.Col(
                        dbc.Nav([
                            dbc.NavLink('Характер', href='/page-2', active='exact', style={'color': '#7B6C63', 'text-align': 'center'}),],
                            pills=True,
                            style={'width': '100%', 'display': 'flex', 'justify-content': 'space-between'}
                            )),
                    dbc.Col(html.Br()),
                    dbc.Col(html.Br()),
                    dbc.Col(html.Br()),
                    dbc.Col(
                        dbc.Nav([
                            dbc.NavLink('Болезни', href='/page-3', active='exact', style={'color': '#7B6C63', 'text-align': 'center'}),],
                            pills=True,
                            style={'width': '100%', 'display': 'flex', 'justify-content': 'space-between'}
                            )),
                    dbc.Col(html.Br()),
                    dbc.Col(html.Br()),
                    dbc.Col(html.Br()),
                    dbc.Col(
                        dbc.Nav([
                            dbc.NavLink('Интересные факты', href='/page-4', active='exact', style={'color': '#7B6C63', 'text-align': 'center'}),],
                            pills=True,
                            style={'width': '100%', 'display': 'flex', 'justify-content': 'space-between'}
                        ),
                        width=True
                    ),
                ],
                align='center',
                className='g-0',
            ),
        ],
        fluid=True,
    ),
    color='D1BFB3',
    style=HEADER_STYLE,
)


content = html.Div(id='page-content', style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id='url'), header, content])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def render_page_content(pathname):
    if pathname == '/':
        return info.layout
    elif pathname == '/page-1':
        return breeds.layout
    elif pathname == '/page-2':
        return character.layout
    elif pathname == '/page-3':
        return illnesses.layout
    elif pathname == '/page-4':
        return facts.layout
    return html.Div(
        [
            html.H1('404: Not found', className='text-danger'),
            html.Hr(),
            html.P(f'The pathname {pathname} was not recognised...'),
        ],
        className='p-3 bg-light rounded-3',
    )

if __name__ == '__main__':
    app.run_server(debug=True)
