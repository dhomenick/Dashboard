import pandas as pd
from pathlib import Path
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# Criando o DataFrame a partir do Excel
data = pd.read_excel('/home/homenick/Projetos/dashboard_jbo/vias do municipio jabaotão.xlsx', sheet_name='vias do municipio jabaotão')

# Manipulando dados
total_pavimentadas = data.loc[data['PAVIMENTO'] == 1, 'PAVIMENTO'].sum()
total_naoPavimentadas = data.loc[data['PAVIMENTO'] == 5, 'PAVIMENTO'].sum()

data["PAVIMENTO"] = data["PAVIMENTO"].replace({1: "não_pavimentada", 5: "pavimentada"})
contagem_pavimento = data.groupby(['BAIRRO', 'PAVIMENTO']).size().unstack(fill_value=0).reset_index()

# Mapa imagem estática
image_path = Path('/home/homenick/Projetos/dashboard_jbo/mapajbo.png')

# Inicializando o aplicativo Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do aplicativo
app.layout = html.Div([
    html.H1("🗺️ Vias Jaboatão dos Guarapes"),
    
    html.Div([
        html.Div([
            html.H2("Total de vias em metro linear"),
            html.P("{:,.2f} m".format(data['COMPRIMENT'].sum()).replace(',', ' ').replace('.', ',')),
        ], className="four columns"),
        
        html.Div([
            html.H2("Total de vias Pavimentadas"),
            html.P("{:,.0f}".format(total_pavimentadas).replace(',', ' ').replace('.', ',')),
        ], className="four columns"),
        
        html.Div([
            html.H2("Total de vias Não Pavimentadas"),
            html.P("{:,.0f}".format(total_naoPavimentadas).replace(',', ' ').replace('.', ',')),
        ], className="four columns"),
    ], className="row"),
    
    dcc.Dropdown(
        id='bairro-dropdown',
        options=[{'label': bairro, 'value': bairro} for bairro in data["BAIRRO"].unique()],
        multi=True,
        placeholder="Escolha o Bairro"
    ),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='pavimento-chart'), width=6),  # Graph on the left
        dbc.Col(html.Img(src=str(image_path), style={'width': '100%', 'height': 'auto'}, alt="mapa de vias"), width=6)  # Image on the right
    ])
])

# Callback para atualizar o gráfico com base na seleção do dropdown
@app.callback(
    Output('pavimento-chart', 'figure'),
    Input('bairro-dropdown', 'value')
)
def update_chart(selected_bairros):
    if not selected_bairros:
        return px.bar(title="Selecione um bairro para ver os dados.")
    
    filtered_data = contagem_pavimento[contagem_pavimento['BAIRRO'].isin(selected_bairros)]
    fig = px.bar(filtered_data, x='BAIRRO', y=['pavimentada', 'não_pavimentada'],
                  title="Contagem de Vias por Bairro",
                  labels={'value': 'Número de Vias', 'BAIRRO': 'Bairro'},
                  barmode="group")
    return fig

# Lançando o webapp
if __name__ == "__main__":
    app.run_server(debug=True)
