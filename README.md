📊 Dashboard Dengue 2024
Este projeto é um painel interativo desenvolvido com Dash e Plotly, que permite a visualização de dados de casos de dengue no Brasil em 2024. Ele oferece gráficos, filtros e indicadores que facilitam a análise epidemiológica da doença.

⚙️ Como instalar as dependências
Recomenda-se o uso de um ambiente virtual (como venv) para manter as dependências isoladas. Execute os seguintes comandos no terminal:

bash
Copiar
Editar
# Crie um ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências do projeto
pip install -r requirements.txt
O arquivo requirements.txt contém:

ini
Copiar
Editar
dash==2.16.1
pandas==2.2.2
plotly==5.20.0
▶️ Como rodar o projeto localmente
Após instalar as dependências, execute o seguinte comando na raiz do projeto:

bash
Copiar
Editar
python app.py
O servidor será iniciado e você poderá acessar o dashboard no navegador pelo endereço:

cpp
Copiar
Editar
http://127.0.0.1:8050
🧰 Ferramentas e versões utilizadas
Python 3.10+

Dash 2.16.1 – Framework para construção de dashboards web com Python.

Plotly 5.20.0 – Biblioteca de visualização de dados.

Pandas 2.2.2 – Análise e manipulação de dados.

📁 Dados exibidos e justificativa
O projeto utiliza um arquivo .csv com dados do SINAN (Sistema de Informação de Agravos de Notificação), focando em casos notificados de dengue em 2024. As seguintes informações são exibidas:

📌 Top 10 municípios com maior número de casos.

📈 Linha do tempo semanal dos casos notificados.

🧬 Distribuição dos tipos de classificação final dos casos (ex: Dengue Clássico, Com Alarme, Grave).

📊 Indicadores:

Número total de casos.

Número de hospitalizações.

Número de óbitos.

Também é possível filtrar os dados por:

Sexo

Faixa etária

Município

Evolução do caso (cura, óbito, etc.)

Classificação final

Hospitalização

Raça/cor

Situação gestacional

Intervalo de datas de notificação
