#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 19:43:09 2022

@author: jrmgarcia
"""

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from datetime import datetime
#import matplotlib.colors mplc
import re

CONFIG = {}
try:
  is_colab = True
  import google.colab
except:
  is_colab = False

def remove_chars(s):
    return re.sub('[^(0-9)^[\,\.,-]', '', s) 

estacoes = pd.read_csv("data/Estacoes.csv", sep=",")
# Iniciar tratamento de dados por causa de digitação errada
estacoes["NOME"] = estacoes["NOME"].str.strip()         # Remove espaços desnecessários do fim e do começo
if estacoes['LAT'].dtype == "O": # não conseguiu converter automaticamente na leitura, algum problema nos dados
   estacoes['LAT'] = estacoes['LAT'].apply(remove_chars).astype(float)   # Mantém apenas caracteres referentes a um número ("-", ".", "," e números 0-9)
if estacoes['LON'].dtype == "O": # idem
   estacoes['LON'] = estacoes['LON'].apply(remove_chars)
qtd_estacoes = len(estacoes) # qtd de estacoes vindas do Forms

# Criei um link simbólico
hist_prec_long = pd.read_csv("data/HIST_PREC_LONG.csv")
hist_prec_long.sort_values(by=["CHAVE", "DATA"], inplace=True)
hist_prec_long["DATA"] = [datetime.strptime(str(dt), "%Y-%m-%d").date() for dt in hist_prec_long["DATA"]]
hist_prec_long.columns = ["CHAVE", "DATA", "VALOR"]

# Deve ter diferentes qtd de linhas para cada estação (simulação da realidade)
#hist_prec_long.groupby(by="CHAVE").count()

#hist_prec_long.dtypes
#hist_prec_wide = pd.read_csv("data/hist_prec_wide.csv", sep=";")
#hist_prec_wide["id"] = hist_prec_wide.index
#hist_prec_wide.sort_values(by="CHAVE", inplace=True)

# range de dias reportados
max_days = (hist_prec_long["DATA"].max() - hist_prec_long["DATA"].min()).days + 1

#cl = hist_prec.columns[1:(hist_prec.shape[1]+1)].values.tolist()
#cl.insert(0, "id")
#hist_prec.columns = cl
#hist_prec.set_index('id', inplace=True, drop=False)


# Define as cores dos marcadores de acordo com os dados
#cmap = mplc.LinearSegmentedColormap.from_list("", ["red", "blue"])
#norm = plt.Normalize(estacoes["VALOR"].min, estacoes["VALOR"].max)
#cmap_acc = cm.LinearColormap(colors=['red', 'blue'], vmin=0,
#                             vmax=np.max(estacoes["VALOR"]))

chroma = "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"  # js lib used for colors

# Search Engine Optimization (SEO). Conjunto de técnicas de otimização para sites, blogs e páginas na web. 
# Essas otimizações visam alcançar bons rankings do conteúdo nas buscas, é uma das principais estratégias do Marketing Digital.
# meta_tags are also required for the app layout to be mobile responsive and is responsible for fitting in mobile screen
meta_tags = [
    {'name': 'viewport',                "content": "width=device-width, initial-scale=1.0"},
    {"name": "author",                  "content": "JRM Garcia"},
    {"name": "title",                   "content": "Projeto Ciência na Escola"},
    {"name": "description",             "content": "Visa engajar e despertar curiosidade científica nos jovens"},
    
    # Google
    {"property": "og:type",             "content": "website"},
    {"property": "og:title",            "content": "Projeto Ciência na Escola"},
    {"property": "og:description",      "content": "Visa engajar e despertar curiosidade científica nos jovens"},
    #{"property": "og:image",            "content": "link-to-image.png"},
    
    # Twitter
    {"property": "twitter:title",       "content": "Projeto Ciência na Escola"},
    {"property": "twitter:description", "content": "Visa engajar e despertar curiosidade científica nos jovens"}
    #{"property": "twitter:image",       "content": "link-to-image.png"},
]

# Nothing will work without a theme
# THEMES ==> https://www.bootstrapcdn.com/bootswatch/
# app = Dash(__name__)   # starts the app
# (and therefore not in the initial layout), i.e., creatinng components on-the-fly
#app.suppress_callback_exception=True


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=meta_tags, 
                #prevent_initial_callbacks=True,
                external_scripts=[chroma])

server = app.server

# Get relative data folder *** NOT WORKING ***
#PATH = pathlib.Path(__file__).parent
#DATA_PATH = PATH.joinpath("../data").resolve()
# dfv = pd.read_csv(DATA_PATH.joinpath("vgsales.csv"))  # GregorySmith Kaggle

