import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# Загружаем данные
df = pd.read_csv('formatted_dog_breeds.csv')
# Уникальные породы собак
breeds = df['Breed'].unique()
default_breed = 'Мастиф', 'Чихуахуа'


aggregated_df = df.groupby('Country of Origin').agg({
    'Breed': lambda x: ', '.join(x),
    'Country of Origin': 'count'
}).rename(columns={'Country of Origin': 'Num_Breeds'}).reset_index()


# Создание круговой диаграммы
figpie = px.pie(aggregated_df, names='Country of Origin', values='Num_Breeds', color_discrete_sequence=px.colors.sequential.RdBu)
figpie.update_layout(title='В какой стране появилось наибольшее количество пород собак?')


# Создание Violin Plot для минимальной продолжительности жизни
fig_min = px.violin(df, y='Min Longevity (yrs)', x='Country of Origin', color='Country of Origin',
                    box=True, points='all', hover_data=df.columns,
                    title='Минимальная продолжительность жизни по странам')


fig_min.update_layout(
    xaxis_title='Страна происхождения',
    yaxis_title='Продолжительность жизни (мин)',
    xaxis={'categoryorder':'total descending'}
)


# Создание Violin Plot для максимальной продолжительности жизни
fig_max = px.violin(df, y='Max Longevity (yrs)', x='Country of Origin', color='Country of Origin',
                    box=True, points='all', hover_data=df.columns,
                    title='Максимальная продолжительность жизни по странам')


fig_max.update_layout(
    xaxis_title='Страна происхождения',
    yaxis_title='Продолжительность жизни (макс)',
    xaxis={'categoryorder':'total descending'}
)
# Словарь коррекции названий стран
country_corrections = {
    'Канада': 'Canada',
    'Германия': 'Germany',
    'Англия': 'UK',
    'Франция': 'France',
    'Мексика': 'Mexico',
    'Шотландия': 'UK',
    'Китай': 'China',
    'Россия': 'Russia',
    'Австралия': 'Australia',
    'Швейцария': 'Switzerland',
    'Ирландия': 'Ireland',
    'Бельгия': 'Belgium',
    'Родезия': 'Rhodesia',
    'США': 'USA',
    'Мадагаскар': 'Madagascar',
    'Италия': 'Italy',
    'Уэльс': 'UK',
    'Ближний Восток': 'Iran',
    'Финляндия': 'Finland',
    'Япония': 'Japan',
    'Нидерланды': 'Netherlands',
    'Венгрия': 'Hungary',
    'Тибет': 'Mongolia',
    'Мальта': 'Malta',
    'Турция': 'Turkey',
    'Африка': 'Egypt',
    'Конго': 'Congo'
}


# Применяем коррекции к столбцу Country of Origin
df['Country of Origin'] = df['Country of Origin'].map(country_corrections)


# Объединяем породы по странам
aggregated_df = df.groupby('Country of Origin').agg({
    'Breed': lambda x: ', '.join(x),
    'Country of Origin': 'count'
}).rename(columns={'Country of Origin': 'Num_Breeds'}).reset_index()


# Создаем текст, который видит пользователь
aggregated_df['hover_text'] = aggregated_df.apply(
    lambda row: f"{row['Country of Origin']}: {row['Breed']}", axis=1
)


# Создаем карту
figmap = px.scatter_geo(aggregated_df, locations="Country of Origin",
                        hover_name="hover_text",  # Пользовательский текст при наведении
                        color="Country of Origin",  # Разные цвета для каждой страны
                        size="Num_Breeds",  # Размер маркеров по количеству пород
                        projection="natural earth",
                        locationmode='country names',
                        size_max=30)  # Увеличение максимального размера маркеров


figmap.update_layout(title='Страны происхождения пород собак')


# Определение макета для Dash
layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H3('Интересные факты'),
                html.Hr(style={'color': '#493B32'}),
            ], style={'textAlign': 'center'})
        )
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=figmap),
        ], width=12),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='breed-dropdown',
                options=[{'label': breed, 'value': breed} for breed in breeds],
                value=default_breed,
                multi=True
            ),
            html.Br(),
            dcc.Graph(id='life-vs-height-graph')
            ], width=6),
        html.Br(),  
          dbc.Col([
            html.Br(),
            html.B(' '),
            html.Br(),
            html.B(' '),
            dcc.Graph(figure=figpie),
        ], width=6),
    ]),
    html.Br(),    
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig_min),
        ], width=6),
        dbc.Col([
            dcc.Graph(figure=fig_max),
        ], width=6),
    ])
], fluid=True)


@callback(
    Output('life-vs-height-graph', 'figure'),
    Input('breed-dropdown', 'value')
)
def update_graph(selected_breeds):
    if not selected_breeds:
        return go.Figure()


    # Фильтрация данных по выбранным породам
    filtered_df = df[df['Breed'].isin(selected_breeds)]


    # Группировка данных по породам для подсчета средних значений
    grouped_df = filtered_df.groupby('Breed').agg({
        'Min Longevity (yrs)': 'mean',
        'Max Longevity (yrs)': 'mean',
        'Min Height (cm)': 'mean',
        'Max Height (cm)': 'mean'
    }).reset_index()


   


    # Создание фигуры Plotly
    fig = go.Figure()


    # Добавление данных о средней продолжительности жизни
    fig.add_trace(go.Scatter(
        x=grouped_df['Breed'],
        y=grouped_df['Min Longevity (yrs)'],
        mode='lines',
        name='Средняя продолжительность жизни',
        line=dict(color='#8DC2E0', width=3),
        stackgroup='one',  # Группировка по оси y
        hoverinfo='text',
        hovertext=f"Порода: {grouped_df['Breed']}<br>Средняя минимальная продолжительность жизни (лет): {grouped_df['Min Longevity (yrs)']}"
    ))


    # Добавление данных о среднем росте
    fig.add_trace(go.Scatter(
        x=grouped_df['Breed'],
        y=grouped_df['Min Height (cm)'],
        mode='lines',
        name='Средний рост',
        line=dict(color='#DE183D', width=3),
        stackgroup='one',  # Группировка по оси y
        hoverinfo='text',
        hovertext=f"Порода: {grouped_df['Breed']}<br>Средняя минимальная продолжительность жизни (лет): {grouped_df['Min Longevity (yrs)']}"
    ))

    # Настройка осей и легенды
    fig.update_layout(
        title='Средняя продолжительность жизни и рост собак',
        xaxis_title='Порода собаки',
        yaxis_title='Среднее значение',
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255, 255, 255, 0.5)', bordercolor='rgba(255, 255, 255, 0.5)')
    )
    return fig
