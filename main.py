import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

# Lê o arquivo CSV
df = pd.read_csv("vacinas_covid_EUA.csv")

# Converte a coluna 'date' no formato datetime
df["date"] = pd.to_datetime(df['date'])

# Exclui linhas com dados ausentes
# df = df.dropna(axis=0)

#---------------------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    html.H2("Vacinas COVID-19 nos Estados Unidos", style={"text-align": "center",
                                                                  "color": "white",
                                                                  "padding-top": "10px"}),

    html.Label("Estado", style={"color": "white", "margin": "0 0 0 3%"}),

    html.Div(children=[
        dcc.Dropdown(
            id='slct_state_dropdown',
            options=[{'label': "Todos", 'value': "Todos"}] + [{'label': state, 'value': state}
                                                            for state in df['state_name'].unique()],
            value='Todos'
        ),
    ], style={'width': "30%",
              "margin": "0 0 0 3%"}),

    html.Div(id='output_container', children=[], style={"color": "white",
                                                        "margin": "0 0 0 3%"}),

    html.Br(),

    html.Div(children=[
        dcc.Graph(id='my_bee_map', figure={}, style={'width': "60%",
                                                     "height": "30%",
                                                     "margin": "0 0 0 3%",
                                                     'border-radius': "10px",
                                                     'overflow': 'hidden'}),

        html.Div(children=[
            html.Div(children=[
                html.Strong("Total da População:"),
                html.Div(id='total_populacao', children=[])
            ], style={'width': "100%",
                      "height": "5vh",
                      "background-color": "black",
                      "text-align": "center",
                      "color": "white",
                      "padding": "5vh 0 5vh 0",
                      'border-radius': "10px"}),

            dcc.Graph(id='graph', figure={}, style={'width': "100%",
                                                    "height": "50vh",
                                                    "margin": "5vh 0 0 0",
                                                    'border-radius': "10px",
                                                    "text-align": "center",
                                                    'overflow': 'hidden'})
        ], style={'width': "40%",
                  "height": "30%",
                  "margin": "0 4% 0 3%"})

    ], style={"display": "flex",
              "justify-content": "space-between"})

], style={'width': "100%",
          "height": "100vh",
          "background": "#1C1C1C",
          "margin": "0 0 0 0",
          "border": "0 0 0 0",
          'overflow': 'hidden',
          "font-family": "Courier, monospace"})

#---------------------------------------------------------------------------------------------

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure'),
     Output(component_id="total_populacao", component_property='children'),
     Output(component_id="graph", component_property='figure')],
     [Input(component_id='slct_state_dropdown', component_property='value')]
)

#---------------------------------------------------------------------------------------------

def update_graph(option_slctd):
    container = "O estado selecionado: {}".format(option_slctd)

    # Filtra o dataframe baseado na seleção do estado
    if option_slctd == "Todos":
        dff = df
    else:
        dff = df[df["state_name"] == option_slctd]

    # Plotly Express Choropleth Map
    fig = px.choropleth(
        dff,
        locationmode='USA-states',
        locations='state_abbreviation',
        scope="usa",
        color='pct_population_series_complete',
        hover_data=['state_abbreviation', 'pct_population_series_complete'],
        color_continuous_scale=px.colors.sequential.BuGn,
        labels={'pct_population_series_complete':'% que completou a série completa de vacinas', 'state_abbreviation':'estado'},
        template='plotly_dark',
        range_color=[0, 100],
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    pop = update_population(option_slctd)

    graph = update_graph(option_slctd)

    return container, fig, pop, graph

#Função para exibir o total da populçao conforme o Dropdown
def update_population(option_slctd):
    # Filtra o dataframe baseado na seleção do estado
    if option_slctd == "Todos":
        pop = df["population"].sum()
    else:
        dff = df[df["state_name"] == option_slctd]
        pop = dff["population"].sum()

    return pop.astype(int)

#Função para exibir o gráfico de barras conforme o Dropdown
def update_graph(option_slctd):
    # Filtra o dataframe baseado na seleção do estado
    if option_slctd == "Todos":
        dff = df
    else:
        dff = df[df["state_name"] == option_slctd]

    graph = px.bar(dff, title="Pessoas que receberam pelo menos uma dose da vacina", template='plotly_dark',
                   x=dff["state_abbreviation"], y=dff["people_received_at_least_one_dose"],
                   labels={'people_received_at_least_one_dose':'quantidade', 'state_abbreviation':'estado'})

    return graph

#---------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
