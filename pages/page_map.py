#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 19:49:04 2022

@author: jrmgarcia
"""
# ***** ATENÇÃO *****      O ID DOS COMPONENTES DEVE SER ÚNICO NO APP INTEIRO

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_leaflet.express as dlx

from datetime import datetime, timedelta, timezone

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash_extensions.javascript import assign

from app import app
from app import max_days
from app import estacoes
#from app import cmap_acc
from app import hist_prec_long as df
#import folium
#from folium.features import ClickForLatLng #, ClickForMarker, LatLngPopup
#import clipboard

# styling the sidebar
SIDEBAR_STYLE = {
   "height": "100vh", 
   "width": "16rem", 
   "position":"fixed"
   #"top": 0,
   #"left": 0,
   #"bottom": 0,
   #"width": "16rem",
   #"padding": "2rem 1rem",
   #"background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
   #"margin-left": "18rem",
   #"margin-right": "2rem",
   "padding": "2rem",
}

# Geojson rendering logic, must be JavaScript as it is executed in clientside.
# ********* ATENÇÃO **** NÃO PODE SER ASSIGNED MAIS DE UMA VEZ ***********
point_to_layer = assign("""function(feature, latlng, context){
    const {min, max, colorscale, circleOptions, colorProp} = context.props.hideout;
    const csc = chroma.scale(colorscale).domain([min, max]);       // chroma lib to construct colorscale
    circleOptions.fillColor = csc(feature.properties[colorProp]);  // set color based on color prop.
    return L.circleMarker(latlng, circleOptions);                  // sender a simple circle marker.
}""")


# Nomes das legendas ao invés de somente a chave
leg_names = dict([est for est in zip(estacoes['CHAVE'].astype("str"), estacoes['NOME'])])

# TODO: Cadastrar escola no mapa
lat_escola = -22.75164732219207
lon_escola = -45.13147045892047

#colorscale = ['red', 'yellow', 'green', 'blue', 'purple']  # rainbow  #cmap_acc
colorscale = ['red', 'green', 'blue', 'purple']  # rainbow  #cmap_acc
#colorscale = px.colors.sequential.Turbo_r

# -----------------------------------------------------------------------------
# Mostra os markers de acordo com a opção escolhida
# -----------------------------------------------------------------------------
#acc_days=1; map_type="AVG"
def getData(acc_days=1, map_type="AVG"):
   dt_last = df["DATA"].max()
   #df.groupby("CHAVE").count()
   dt_1st  = dt_last - timedelta(days=acc_days-1)
   mask = (df['DATA'] >= dt_1st) & (df['DATA'] <= dt_last)
   
   dff = pd.DataFrame(estacoes[["CHAVE", "NOME"]])
   dff = pd.merge(dff, df.loc[mask, ["CHAVE", "VALOR"]].groupby(by="CHAVE").mean(numeric_only=True), 
                  how="left", on="CHAVE")
   dff = pd.merge(dff, df.loc[mask, ["CHAVE", "VALOR"]].groupby(by="CHAVE").count().rename(columns={'VALOR':'OCORR'}),
         how="left", on="CHAVE")
   
   dff.set_index('CHAVE', inplace=True)
   dff["CHAVE"] = dff.index
   dff["CHAVE2"] = [f"{x+1}-{dff['NOME'][x]}" for x in range(len(dff))]

   vmax_val  = df.groupby(by="CHAVE").mean(numeric_only=True)["VALOR"].max()    
   vmax_ocor = max_days
   
   if map_type == "AVG":
      vmax = vmax_val
      color_prop = 'VALOR'
   else:
      vmax = vmax_ocor
      color_prop = 'OCORR'
      
   dicts = estacoes.to_dict(orient='records')
   #item=dicts[0]
   for item in dicts:
       try:
          item[color_prop] = dff.loc[item["CHAVE"]][color_prop]   # muda valor das estações
          item["tooltip"] = "{}-{} ({:.1f})".format(item['CHAVE'], item['NOME'], item[color_prop])  # bind tooltip
       except:
          item[color_prop] = None
          item["tooltip"] = "{}-{} ({})".format(item['CHAVE'], item['NOME'], item[color_prop])  # bind tooltip

   geojson = dlx.dicts_to_geojson(dicts, lon="LON", lat="LAT")    # convert to geojson
   geobuf = dlx.geojson_to_geobuf(geojson)  # convert to geobuf
   #print("**** vmax:", vmax)
   #print(dff)
   #print(geojson)

   colorbar = dl.Colorbar(colorscale=colorscale, width=20, height=150, min=0, max=vmax, unit='mm/dia')
   # Geojson rendering logic, must be JavaScript as it is executed in clientside.
   # Create geojson.
   
   datas = f'''{dt_1st:%d-%m-%Y} à {dt_last:%d-%m-%Y}'''
   
   return(geobuf, vmax, colorbar, datas, dff)

geobuf, vmax, colorbar, datas, DF = getData()

#print("**** id geojson:", id(geojson), " id colorbar:", id(colorbar))

geojson = dl.GeoJSON(data=geobuf, format="geobuf", id="layer_geojson",
           zoomToBounds=True,  # when true, zooms to bounds when data changes
           options=dict(pointToLayer=point_to_layer),  # how to draw points
           cluster=False, superClusterOptions=dict(radius=(5)),         # adjust cluster size
           hideout=dict(colorProp="VALOR", circleOptions=dict(fillOpacity=.7, stroke=False, radius=5, id="xxx"),
                         min=0, max=vmax, colorscale=colorscale))

sidebar = dbc.Card([
   dbc.CardBody([
      #html.P("Opção de visualização", 
      #       style={"font-weight": "bold"}),
      #dbc.RadioItems(id="mapType", options=[{"label":"Acumulado" , "value":"AVG"},
      #                                      {"label":"Ocorrência", "value":"FREQ"}],
      #               value="AVG", persistence=True, persistence_type="memory"),
      #
      #html.Hr(),
      dbc.InputGroup([
         dbc.Label(children={}, id="txtMaptype", style={"display":"inline-block", "font-weight": "bold"}),
         dcc.Input(id="accDays", type="number", min=1, max=max_days, value=1, step=1, 
                persistence=True, persistence_type="session", style={"display":"inline-block", "width": "60px"}),
         dbc.Label("dias", style={"display":"inline-block", "font-weight": "bold"})]),
      html.Hr(),
      html.Pre(id="out_datas", children={}, 
               style={"color":"blue"}),
      html.Hr(),
      html.P("Tamanho das estações", 
             style={"font-weight": "bold"}),
      dcc.Slider(min=1, max=100, step=5, value=20, id='slider_raio', 
                 marks=dict([(str(x), str(x)) for x in range(0, 101, 20)])),
      html.Hr(),
      #html.Hr(),
      #dbc.Checkbox(id="doCluster", label="Agrupa estações", value=False)
   ]),
   ], 
   style=SIDEBAR_STYLE)

content = html.Div([
   dbc.Row([
      dbc.Col([
         dcc.Dropdown(id='dropdown-estacoes', clearable=False, multi=True,
                        options=[{'label': str(x[0])+"-"+x[1], 'value': x[0]} for x in sorted(estacoes.loc[:, ['CHAVE', 'NOME']].values.tolist())],
                        value=[]),
         html.P(),
         dl.Map(
            dl.LayersControl(
               [dl.BaseLayer(dl.TileLayer(), name="Mapa básico", checked=True)] +
               [dl.Overlay(children=geojson, name="Estações", checked=True),
                dl.Overlay(children=dl.Marker(position=(lat_escola, lon_escola), title="EERB", alt="EERB"), name="Escola", checked=True),
                dl.Overlay(children=colorbar, id="layer_cbar", name="Escala", checked=True)]),
            style={'width': '100%', 'height': '80vh', 'margin': "auto", "display": "block"},
            id="map_est")
         ], width=8
      ),
      dbc.Col([
         html.Div(id="plot_bar_ocor", children={}),
         html.Div(id="plot_bar_acum", children={}),
      ], width=4)
   ]),
   dbc.Row([
      dbc.Col(
         html.Div(id="plot_hist_est", children={}),
         width=8
      ),
   ])
], style=CONTENT_STYLE)


#
layout = dbc.Container([
    dbc.Row([
       dbc.Col(sidebar, width=2),
       dbc.Col(content, width=10)#, style={"margin-left": "16rem"})
    ])
], fluid=True)

# -----------------------------------------------------------------------------
# Callback de colorização dos markers, de acordo com as opções
# -----------------------------------------------------------------------------
@app.callback([Output("layer_geojson", "data"),
               Output("layer_geojson", "hideout"),
               Output("layer_cbar", "children"),
               Output("out_datas", "children"),
               Output("txtMaptype", "children"),
               Output("plot_bar_ocor", "children"),
               Output("plot_bar_acum", "children")],
              [Input("accDays", "value"),
               Input("slider_raio", "value")])
#acc_days=5
def colorMarker(acc_days, raio):  # AVG | FREQ
    print("**** Função colorMarker(BEGIN)")
    map_type = "AVG"
    #data = getData(acc_days, map_type)
    geobuf, vmax, colorbar, datas, DF = getData(acc_days, map_type)

    ret0 = geobuf

    ret1 = dict(colorProp="VALOR" if map_type == "AVG" else "OCORR", 
                circleOptions=dict(fillOpacity=.7, stroke=False, radius=raio),
                min=0, max=vmax, colorscale=colorscale) # hideout
    ret2 = colorbar # colorbar
    ret3 = datas    # texto datas
    
    if map_type == "AVG":
       ret4 = "Chuva acumulada dos últimos "
    else:
       ret4 = "Núm. de registros de chuva dos últimos "
       
    dias_str = f"{acc_days} dia{'s' if acc_days > 1 else ''}"

    # BAR CHART - OCORRÊNCIAS
    fig = px.bar(DF, x="CHAVE2", y='OCORR', hover_data={"CHAVE":True, "CHAVE2":False},
                 color="VALOR", color_continuous_scale=px.colors.sequential.Sunsetdark, #colorscale,
                 barmode="group", range_color=[0, int(max(DF.VALOR))])
    fig.update_layout(title_text=f"<b>Medições por pluviômetro em {dias_str}</b>", 
                      font=dict(size=14, color="RebeccaPurple"),
                      coloraxis_colorbar_title_text = "Chuva média",
                      title_x=0.5, title_y=0.92)
    fig.update_xaxes(title='RA do aluno')
    fig.update_yaxes(title='Qtd medições')

    #fig.update_xaxes(font_size=16)
    #fig.show()  # opens a browser tab
    # fig.update_coloraxes(showscale=False) # - YES!
    
    ret5 = dcc.Graph(figure=fig)
    
    # BAR CHART - ACUMULADO

    # If color is continuous, falls back to stacked bar chart
    # df_['model_cycle'] = df_['model_cycle'].astype(str)
   # Categorical colorbar is not scale
   # import string
   #DF["VALOR_CUT"] = np.array(list('0'+string.ascii_uppercase))[DF.VALOR.round(0).fillna(0).astype(int).to_list()]
   # DF["OCORR_CUT"] = np.array(list('0'+string.ascii_uppercase))[DF.OCORR.round(0).fillna(0).astype(int).to_list()]

    fig2 = px.bar(data_frame=DF, x="CHAVE2", y="VALOR", hover_data={"CHAVE":True, "CHAVE2":False},
                 color="OCORR", #, color_continuous_scale=px.colors.sequential.Turbo_r, #colorscale,
                 barmode="group", range_y=[0, int(max(DF.VALOR))+2], range_color=[0, int(max(DF.OCORR))+2])
    fig2.update_layout(title_text=f"<b>Chuva média de {dias_str} por pluviômetro</b>", 
                      font=dict(size=14, color="RebeccaPurple"),
                      coloraxis_colorbar_title_text = "Medições",
                      title_x=0.5, title_y=0.92)
    fig2.update_xaxes(title='RA do aluno')
    fig2.update_yaxes(title='(mm/dia)')

    #fig2.data[0].x = DF["NOME"]
    #fig2.data[0].alignmentgroup = False
    #fig2.show()  # opens a browser tab
    #fig2.update_coloraxes(showscale=False) # - YES!
    
    ret6 = dcc.Graph(figure=fig2)

    
    return(ret0, ret1, ret2, ret3, ret4, ret5, ret6)
    

# -----------------------------------------------------------------------------
# Chainned callbacks
# Callback quando clicar em alguma feature atualiza o dropdown de estações
# -----------------------------------------------------------------------------
@app.callback(Output("dropdown-estacoes", "value"),
              [Input("layer_geojson", "click_feature"),
               Input("dropdown-estacoes", "value")])
def feature_click(feature, lista_est):
    print("**** Função feature_click(BEGIN)")
    ctx = dash.callback_context
    compo = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if feature is not None and feature['properties']['cluster'] == False and compo=="layer_geojson":
       chave_est = feature['properties']['CHAVE']
       if lista_est is not None:
          if chave_est in lista_est:
             lista_est.remove(chave_est)
          else:
             lista_est.append(chave_est)
       else:
          lista_est = [chave_est]
    
    return(lista_est)

# -----------------------------------------------------------------------------
# Callback quando alterar o dropdown
# -----------------------------------------------------------------------------
@app.callback(Output("plot_hist_est", "children"),
              [Input("dropdown-estacoes", "value"),
               Input("accDays", "value")])
def dropdown_click(lista_est, acc_days):
    print("**** Função dropdown_click(BEGIN)")
    if lista_est != None and len(lista_est) > 0:
       
       # if lista_est_values != lista_est_values_atu:
       lista_est = sorted(lista_est)
      
       #lista_est = [1, 2]
       dff = df[df["CHAVE"].isin(lista_est)].copy().sort_values(by="DATA")
       dmin = dff["DATA"].min()
       dmax = dff["DATA"].max()
       
       # É preciso criar dados (eixo Y) com valores nulos (NaN) para que os gaps sejam mostrados: :(
       x = [dmin+timedelta(days=x) for x in range((dmax-dmin).days)]  # todos os dias, do primeiro ao último
       
       # Cria um DF completo, todos os dias para todas as estações a serem plotadas
       DF = pd.DataFrame(np.array(np.meshgrid(lista_est, x)).reshape(2, len(lista_est)* len(x)).T)
       DF.columns = ["CHAVE", "DATA"]  # iguala as columnas para fazer o merge
       
       #pd.set_option('display.max_rows', None)
       # O merge com join=left cria dados em branco para VAL_PREC quando não encontrado no DF completo (que está à esquerda do comando)
       dff = pd.merge(DF, dff, how="left")  
       
       fig = px.line(data_frame=dff, x="DATA", y="VALOR", color="CHAVE", markers=True,
                     title="<b>Série temporal completa (dias considerados está entre área tracejada)</b>")
       #fig.update_traces(connectgaps=False)
       fig.update_layout(xaxis_title="Dias", 
                         yaxis_title="Valor informado",
                         #plot_bgcolor='black',
                         title_x=0.5, title_y=0.85)
       fig.for_each_trace(lambda t: t.update(name = leg_names[t.name]))
       fig.add_vrect(type="rect", x0=dmax - timedelta(days=acc_days), x1=dmax, 
                     fillcolor="lightgrey", opacity=0.4, 
                     line_color="black", line_width=2, line_dash="dash")
       fig.update_shapes(layer="below")
       
       return(dcc.Graph(figure=fig))

