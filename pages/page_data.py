#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 19:49:04 2022

@author: jrmgarcia
"""
# https://hackerthemes.com/bootstrap-cheatsheet/
# ***** ATENÇÃO *****      O ID DOS COMPONENTES DEVE SER ÚNICO NO APP INTEIRO

from dash import html, Input, Output, dash_table as dt
#from table_bars import data_bars
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
#import le_planilha
from app import hist_prec_wide as df
from app import app

prec_max = df.max().max()
initial_active_cell = {"row": 0, "column": 0, "column_id": "id", "row_id": 0}

layout = html.Div([
    html.Div([dbc.Label("Valor mínimo:")], style={'display': 'inline-block'}),
    
    html.Div([
       dbc.Input(id="valMin", type="number", min=0, max=prec_max, value=0, step=1,
                 persistence=True, persistence_type="session")],
       style={'display':'inline-block', "margin-left":"15px"}),
    
    html.Div([
       dbc.Label("Valor máximo:")],
       style={'display':'inline-block', "margin-left":"15px"}),
    
    html.Div([
       dbc.Input(id="valMax", type="number", min=0, max=prec_max, value=prec_max, step=1,
                 persistence=True, persistence_type="session")],
       style={'display':'inline-block', "margin-left":"15px"}),
 
    html.Div(
      dt.DataTable(id='datatable', 
         columns=[{'name': i, 'id': i, 'deletable': True} for i in df.columns],
         data=df.to_dict('records'),
         editable=False,
         page_action='native',
         page_size=50,
         #sort_action="native",
         active_cell=initial_active_cell,
         style_data_conditional=(
            # list 1
            [
               # Possible keys for the "ïf" statements
               # . filter_query = conditions
               # . column_id = column to apply the style (otherwise, the entire row
               # . column_type, row_index, state, column_editable

               # Dict - Align text to the left ******************************
               {
                  'if': {
                     'column_type': 'text'
                     # 'text' | 'any' | 'datetime' | 'numeric'
                  },
                  'textAlign': 'left'
               },
               # Dict: Format active cells *********************************
               {  
                  'if': {
                     'state': 'active'  # 'active' | 'selected'
                  },
                  'border': '3px solid yellow', #rgb(0, 116, 217)'
                  'row_id': '2'
               }
            ]
         
            + # Combine lists with "+"
            
            # if inside a list comprehention
            [   # Highlighting largest value in each column ********
               {
                  'if': {
                     # since using .format, escape { with {{
                     'filter_query': '{{{}}} >= {}'.format(col, value),
                     'column_id': col
                  },
                  #'backgroundColor': 'black',
                  'color': 'blue'
               } for (col, value) in df.max()[1:(df.shape[1]+1)].iteritems() 
            ]
            
            + # Combine lists with "+"
         
            # if inside a list comprehention
            [   # Blanking min/max filtered values
               {
                  'if': {
                     'filter_query': '{{{}}} is blank'.format(col),
                     'column_id': col
                  },
                  #'backgroundColor': '#B10DC9',
                  'color': 'white'
               } for col in df.columns
            ]
            # Adding data bars to numerical columns (via function) ***************
            #data_bars(df, 'Serial number')
         ) # style_data_cond
      ) # dt
   ) # html.div (dt)
])
@app.callback(
   Output(component_id='datatable', component_property='data'),
   [Input(component_id='valMin', component_property='value'),
    Input(component_id='valMax', component_property='value'),
    Input(component_id='datatable', component_property='active_cell'),
    Input(component_id='datatable', component_property='derived_virtual_row_ids')])
def update_table(valMin, valMax, active_cell, row_ids):
   
   # is None at the 1st render because they are rows AFTER filtering|sorting
   if row_ids is None:
      row_ids = df['id']
      
   res = df.iloc[:,1:(df.shape[1]-1)]
       
   # else:
   #     res = df.loc[row_ids].iloc[:,1:(df.shape[1]-1)]
   
   # Filtra os dados de acordo com os valores min/max
   res = pd.DataFrame(np.where((res < valMin) | (res > valMax), None, res))
   res = pd.concat([df.loc[row_ids]["CHAVE"], res, df.loc[row_ids]["id"]], axis=1)        
   res.columns = df.columns
     
   return res.to_dict("records")

