# Imports
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import os

# Caminho
path = "C:/Users/Cleber/Desktop/Vinicius/DashBoard_Inegrador/archive"
csv_file = os.path.join(path, "sinan_dengue_sample_2024.csv")

# Colunas usadas
colunas_usadas = [
    'MUNICIPIO', 'UF', 'CS_SEXO', 'NU_IDADE_N', 'EVOLUCAO',
    'CLASSI_FIN', 'HOSPITALIZ', 'DT_OBITO', 'DT_NOTIFIC',
    'CS_RACA', 'CS_GESTANT'
]

chunk_size = 100000
chunks = pd.read_csv(csv_file, usecols=colunas_usadas, chunksize=chunk_size, low_memory=False)
df = pd.concat(chunks)

# Preparo dos dados
df['MUNICIPIO'] = df['MUNICIPIO'].fillna('').astype(str)
df['UF'] = df['UF'].fillna('').astype(str)
df['municipio_uf'] = df['MUNICIPIO'] + " (" + df['UF'] + ")"

# Corrigido: garantir que NU_IDADE_N é numérico
df['NU_IDADE_N'] = pd.to_numeric(df['NU_IDADE_N'], errors='coerce')

# Corrigido: função segura para extrair idade
def extrair_idade(valor):
    if pd.notna(valor) and valor >= 4000:
        return int(valor % 100)
    return None

df['IDADE_ANOS'] = df['NU_IDADE_N'].apply(extrair_idade)
df['DT_NOTIFIC'] = pd.to_datetime(df['DT_NOTIFIC'], errors='coerce')
df['SEMANA'] = df['DT_NOTIFIC'].dt.isocalendar().week

# Mapas
racas = {1: "Branca", 2: "Preta", 3: "Amarela", 4: "Parda", 5: "Indígena", 9: "Ignorado"}
gestantes = {1: "1º trimestre", 2: "2º trimestre", 3: "3º trimestre", 4: "Ignorada", 5: "Não gestante", 6: "Não aplicável", 9: "Ignorado"}
mapa_evolucao = {1: "Cura", 2: "Óbito por Dengue", 3: "Óbito outras causas", 4: "Em investigação", 9: "Ignorado"}
mapa_classificacao = {5: "Descartado", 10: "Dengue", 11: "Com Alarme", 12: "Grave", 13: "Chikungunya"}

df['evolucao_nome'] = df['EVOLUCAO'].map(mapa_evolucao)
df['classificacao_nome'] = df['CLASSI_FIN'].map(mapa_classificacao)
df['raca_nome'] = df['CS_RACA'].map(racas)
df['gestante_nome'] = df['CS_GESTANT'].map(gestantes)

# App
app = dash.Dash(__name__)
app.title = "Dashboard Dengue 2024"

# Layout
app.layout = html.Div(style={'display': 'flex', 'minHeight': '100vh'}, children=[
    html.Div([
        html.H2("🧪 Filtros", style={'color': 'white', 'textAlign': 'center'}),
        html.Label("👫 Sexo:", style={'color': 'white'}),
        dcc.Dropdown(id='sexo', options=[
            {'label': 'Masculino', 'value': 'M'},
            {'label': 'Feminino', 'value': 'F'},
            {'label': 'Ignorado', 'value': 'I'}
        ], placeholder="Todos"),

        html.Label("🎂 Faixa Etária:", style={'color': 'white', 'marginTop': '10px'}),
        dcc.Dropdown(id='faixa_etaria', options=[
            {'label': '0-9 anos', 'value': '0-9'},
            {'label': '10-19 anos', 'value': '10-19'},
            {'label': '20-39 anos', 'value': '20-39'},
            {'label': '40-59 anos', 'value': '40-59'},
            {'label': '60+ anos', 'value': '60+'}
        ], placeholder="Todas"),

        html.Label("🏙️ Município:", style={'color': 'white', 'marginTop': '10px'}),
        dcc.Dropdown(id='municipio', options=[{'label': x, 'value': x} for x in sorted(df['municipio_uf'].unique())], placeholder="Todos"),

        html.Label("📈 Evolução:", style={'color': 'white', 'marginTop': '10px'}),
        dcc.Dropdown(id='evolucao', options=[{'label': v, 'value': k} for k, v in mapa_evolucao.items()], placeholder="Todas"),

        html.Label("🔍 Classificação Final:", style={'color': 'white', 'marginTop': '10px'}),
        dcc.Dropdown(id='classificacao', options=[{'label': v, 'value': k} for k, v in mapa_classificacao.items()], placeholder="Todas"),

        html.Label("🏥 Hospitalizado:", style={'color': 'white', 'marginTop': '10px'}),
        dcc.Dropdown(id='hospitalizado', options=[
            {'label': 'Sim', 'value': 1},
            {'label': 'Não', 'value': 2}
        ], placeholder="Todos"),

        html.Label("🧬 Raça/Cor:", style={'color': 'white', 'marginTop': '10px'}),
        dcc.Dropdown(id='raca', options=[{'label': v, 'value': k} for k, v in racas.items()], placeholder="Todas"),

        html.Label("🤰 Gestante:", style={'color': 'white', 'marginTop': '10px'}),
        dcc.Dropdown(id='gestante', options=[{'label': v, 'value': k} for k, v in gestantes.items()], placeholder="Todas"),

        html.Label("📆 Período de Notificação:", style={'color': 'white', 'marginTop': '10px'}),
        dcc.DatePickerRange(
            id='data_range',
            start_date=df['DT_NOTIFIC'].min(),
            end_date=df['DT_NOTIFIC'].max(),
            display_format='DD/MM/YYYY',
            style={'marginTop': '5px'}
        ),


    ], style={'width': '22%', 'padding': '20px', 'backgroundColor': '#2c3e50'}),

      

    html.Div([
        html.H1("📊 Painel Dengue 2024", style={'textAlign': 'center', 'marginBottom': '20px'}),

        html.Div([
            dcc.Graph(id='grafico-municipio'),
            dcc.Graph(id='grafico-linha'),
            dcc.Graph(id='grafico-pizza'),
        ], style={'display': 'block'}),

        html.Div(id='indicadores', style={'display': 'flex', 'justifyContent': 'space-around', 'marginTop': '30px'})
    ], style={'width': '78%', 'padding': '20px', 'backgroundColor': '#ecf0f1'})
])

# Callback# Callback único e correto
@app.callback(
    [Output('grafico-municipio', 'figure'),
     Output('grafico-linha', 'figure'),
     Output('grafico-pizza', 'figure'),
     Output('indicadores', 'children')],
    [Input('sexo', 'value'),
     Input('faixa_etaria', 'value'),
     Input('municipio', 'value'),
     Input('evolucao', 'value'),
     Input('classificacao', 'value'),
     Input('hospitalizado', 'value'),
     Input('raca', 'value'),
     Input('gestante', 'value'),
     Input('data_range', 'start_date'),
     Input('data_range', 'end_date')]
)
def atualizar(sexo, faixa, municipio, evolucao, classificacao, hospitalizado, raca, gestante, data_ini, data_fim):

    filtro = df.copy()

    if data_ini and data_fim:
        filtro = filtro[(filtro['DT_NOTIFIC'] >= data_ini) & (filtro['DT_NOTIFIC'] <= data_fim)]


    if sexo: filtro = filtro[filtro['CS_SEXO'] == sexo]
    if faixa:
        if faixa == '0-9': filtro = filtro[(filtro['IDADE_ANOS'] >= 0) & (filtro['IDADE_ANOS'] <= 9)]
        elif faixa == '10-19': filtro = filtro[(filtro['IDADE_ANOS'] >= 10) & (filtro['IDADE_ANOS'] <= 19)]
        elif faixa == '20-39': filtro = filtro[(filtro['IDADE_ANOS'] >= 20) & (filtro['IDADE_ANOS'] <= 39)]
        elif faixa == '40-59': filtro = filtro[(filtro['IDADE_ANOS'] >= 40) & (filtro['IDADE_ANOS'] <= 59)]
        elif faixa == '60+': filtro = filtro[(filtro['IDADE_ANOS'] >= 60)]
    if municipio: filtro = filtro[filtro['municipio_uf'] == municipio]
    if evolucao: filtro = filtro[filtro['EVOLUCAO'] == evolucao]
    if classificacao: filtro = filtro[filtro['CLASSI_FIN'] == classificacao]
    if hospitalizado: filtro = filtro[filtro['HOSPITALIZ'] == hospitalizado]
    if raca: filtro = filtro[filtro['CS_RACA'] == raca]
    if gestante: filtro = filtro[filtro['CS_GESTANT'] == gestante]

    # Gráfico de barras - Top 10 municípios
    top_municipios = filtro['municipio_uf'].value_counts().nlargest(10).reset_index()
    top_municipios.columns = ['Município', 'Casos']
    fig_municipio = px.bar(
        top_municipios,
        x='Casos',
        y='Município',
        orientation='h',
        title='🏙️ Top 10 Municípios com Mais Casos',
        color_discrete_sequence=['#3498db']  
    )

    fig_municipio.update_layout(yaxis=dict(autorange='reversed'), plot_bgcolor='#ffffff')

    # Linha semanal
    semana = filtro.groupby('SEMANA').size().reset_index(name='casos')
    fig_linha = px.line(semana, x='SEMANA', y='casos', markers=True, title='📅 Casos por Semana')

    # Pizza classificação
    pizza = filtro['classificacao_nome'].value_counts().reset_index()
    pizza.columns = ['Classificação', 'Casos']
    fig_pizza = px.pie(pizza, values='Casos', names='Classificação', title='🧬 Classificação Final')

    # Indicadores
    total = filtro.shape[0]
    hosp = filtro['HOSPITALIZ'].sum()
    obitos = filtro['DT_OBITO'].notna().sum()

    cards = [
        html.Div([html.H3(f"{total:,}"), html.P("Casos Totais")], style={'backgroundColor': '#dfe6e9', 'padding': '20px', 'borderRadius': '10px', 'width': '30%', 'textAlign': 'center'}),
        html.Div([html.H3(f"{hosp:,}"), html.P("Hospitalizações")], style={'backgroundColor': '#ffeaa7', 'padding': '20px', 'borderRadius': '10px', 'width': '30%', 'textAlign': 'center'}),
        html.Div([html.H3(f"{obitos:,}"), html.P("Óbitos")], style={'backgroundColor': '#fab1a0', 'padding': '20px', 'borderRadius': '10px', 'width': '30%', 'textAlign': 'center'}),
    ]

    return fig_municipio, fig_linha, fig_pizza, cards



# Run
if __name__ == '__main__':
    app.run(debug=True)
