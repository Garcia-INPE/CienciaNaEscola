#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 19:45:11 2022
@author: jrmgarcia
"""
# ***** ATENÇÃO *****      O ID DOS COMPONENTES DEVE SER ÚNICO NO APP INTEIRO


from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
#import plotly.express as px  # (version 4.7.0 or higher)

# Connect to main app.py file
from app import app
from app import server

app.title = "Ciência na escola"

# Connect to your app pages
from pages import page_map #, page_data
from app import estacoes
from app import max_days


# ABOUT dcc.Store -------------------------------------------------------------
# . shared data among pages up to 10MB 
# . can only stored: dictionary | list | number | string (including dict|list entries)
# . must be in app.py or index.py, i.e., the executable script where there is:
#   if __name__=='__main__': app.run_server(...)
# Will be shared via dcc.Store ------------------------------------------------

app.layout = dbc.Container([
   #dcc.Store(id="CONFIG", data=CONFIG),   # Share CONFIG among app pages
   dcc.Location(id="url"), # elemento invisível
   dbc.Row([
      html.H2("Projeto pluviômetro na Escola - EE Regina Bartelega - INPE", className='text-center text-primary mb-4'),
      html.H4(f"Total de pluviômetros: {len(estacoes)} - Total de dias reportados: {max_days}", className='text-center text-primary mb-4')
      ]
      #dbc.Button(title="Ler planilha", id='btGetData',  n_clicks=0, size="lg")],
   ), # 1st row
   
   dbc.Row(
      dbc.Col([
         #dbc.Nav([
         #   dbc.NavLink("Mapa"          , href="/" , active="exact"),
         #   #dbc.NavLink("Dados"         , href="/dados", active="exact"),
         #   ],
         #   vertical=False, pills=True,
         #),
         # dbc.Tabs([
         #    dbc.Tab(label="Mapa", tab_id="tab_map"),
         #    dbc.Tab(label="Dados", tab_id="tab_data"),
         #    dbc.Tab(label="Série Temporal", tab_id="tab_st")],
         #    id="tabs",
         #    active_tab="tab_map",
         # ),
         html.Div(id="tab-content", className="p-2", children=[page_map.layout]), # children is optional
      ], width=12)
   ) # 2nd row
], fluid=True)

#@app.clientside_callback
#@app.callback(Output(component_id='tab-content', component_property='children'),
#              #[Input(component_id='btGetData', component_property='n_clicks'),
#              [Input(component_id="url", component_property="pathname")])
#def display_page(pathname):
#    if pathname == '/':
#       return page_map.layout
#    #if pathname == '/dados':
#    #   return page_data.layout
#    else:
#       return "404 Page Error! Please choose a link"

# Needed to run this script
if __name__=='__main__':
    app.run_server(debug=True, host="127.0.0.1", port=8080)
    #app.server.run(debug=True, port=8000, host="0.0.0.0")
    # Usando este abaixo dá erro de ID do callback not found
    # run_server() faz mais consas antes de chamar server.run()
    #app.run_server(debug=True, port=8000, host="127.0.0.1")
