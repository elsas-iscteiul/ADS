import dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import json



def draw(df):

    dff = df.drop('index', 1)
    dff = dff.groupby(['algorithm']).agg(['mean','median','std']).transpose()
    dff = dff.reset_index()
    dff.rename(columns = {'level_0':'field','level_1':'statistic'}, inplace=True)

    app = DjangoDash('DashApp')

    app.layout = html.Div([
        html.Label('Algoritmos'),
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': 'ADAM','value':'ADAM'},
                {'label': 'ADAMW','value':'ADAMW'},
                {'label': 'RADAM','value':'RADAM'},
                {'label': 'RMSprop','value':'RMSprop'},
                {'label': 'SGD','value':'SGD'},
                {'label': 'All','value':'All'}
            ],
        ),
        html.Label('x'),
        dcc.Dropdown(
            id='x_type',
            options=[
                {'label':'accuracy', 'value':'accuracy'},
                {'label':'loss', 'value':'loss'},
                {'label':'val_accuracy', 'value':'val_accuracy'},
                {'label':'val_loss', 'value':'val_loss'}
            ],
        ),
        html.Label('y'),
        dcc.Dropdown(
            id='y_type',
            options=[
                {'label':'accuracy', 'value':'accuracy'},
                {'label':'loss', 'value':'loss'},
                {'label':'val_accuracy', 'value':'val_accuracy'},
                {'label':'val_loss', 'value':'val_loss'},
            ],
        ),


        html.Label('z'),
        dcc.Dropdown(
            id='z_type',
            options=[
                {'label':'accuracy', 'value':'accuracy'},
                {'label':'loss', 'value':'loss'},
                {'label':'val_accuracy', 'value':'val_accuracy'},
                {'label':'val_loss', 'value':'val_loss'},
            ],
        ),


        html.Label('w'),
        dcc.Dropdown(
            id='w_type',
            options=[
                {'label':'accuracy', 'value':'accuracy'},
                {'label':'loss', 'value':'loss'},
                {'label':'val_accuracy', 'value':'val_accuracy'},
                {'label':'val_loss', 'value':'val_loss'},
            ],
        ),
        html.Div("clickData"),
        dcc.Markdown(
            id="click-data",
            ),
                
            
        
        html.Label('Gráfico'),
        dcc.Dropdown(
            id='u_type',
            options=[
                {'label':'3d_symbol', 'value':'3d_symbol'},
                {'label':'3d_size', 'value':'3d_size'},
                {'label':'subplot', 'value':'subplot'},
                {'label':'animated_subplot', 'value':'animated_subplot'},
                
            ],
        ),
        
        html.Label('ADAM Color'),
        dcc.Dropdown(
            id='color_ADAM',
            options=[
                {'label':'red', 'value':'red'},
                {'label':'green', 'value':'green'},
                {'label':'yellow', 'value':'yellow'},
                {'label':'blue', 'value':'blue'},
                {'label':'pink', 'value':'pink'},
                
            ],
        ),
        
        html.Label('ADAMW Color'),
        dcc.Dropdown(
            id='color_ADAMW',
            options=[
                {'label':'red', 'value':'red'},
                {'label':'green', 'value':'green'},
                {'label':'yellow', 'value':'yellow'},
                {'label':'blue', 'value':'blue'},
                {'label':'pink', 'value':'pink'},
                
            ],
        ),
        
        html.Label('RADAM Color'),
        dcc.Dropdown(
            id='color_RADAM',
            options=[
                {'label':'red', 'value':'red'},
                {'label':'green', 'value':'green'},
                {'label':'yellow', 'value':'yellow'},
                {'label':'blue', 'value':'blue'},
                {'label':'pink', 'value':'pink'},
                
            ],
        ),
        
        html.Label('RMSprop Color'),
        dcc.Dropdown(
            id='color_RMSprop',
            options=[
                {'label':'red', 'value':'red'},
                {'label':'green', 'value':'green'},
                {'label':'yellow', 'value':'yellow'},
                {'label':'blue', 'value':'blue'},
                {'label':'pink', 'value':'pink'},
                
            ],
        ),
        
        html.Label('SGD Color'),
        dcc.Dropdown(
            id='color_sgd',
            options=[
                {'label':'red', 'value':'red'},
                {'label':'green', 'value':'green'},
                {'label':'yellow', 'value':'yellow'},
                {'label':'blue', 'value':'blue'},
                {'label':'pink', 'value':'pink'},
                
            ],
        ),
        
        dcc.Graph(id='desenho'),
        html.Label('Estatisticas'),
        dash_table.DataTable(
            id = 'table',
            columns = [{'name': i, 'id': i} for i in dff.columns],
            data = dff.to_dict('records')
            
        ),
        
        
        
        ##dcc.Graph(id='Data'
        ##),
        ##html.Div(
        ##    html.Pre(id='click-data', style={'display' : 'none'})
        ##),
        
        html.Div(id='intermediary', style={'display' : 'none'}),
        

    ])


    
    @app.callback(
    Output('intermediary','children'),
    [Input('dropdown','value')]
    )
    
    def update_algs(alg):
        if alg != 'All':
            df_1 = df[df['algorithm'] == alg]
        else:
            df_1 = df

        return df_1.to_json()
        


  
    @app.callback(
    Output('desenho','figure'),
    [Input('x_type','value'),
    Input('y_type','value'),
    Input('z_type','value'),
    Input('w_type','value'),
    Input("u_type","value"),
    Input('intermediary','children'),
    Input("color_ADAM","value"),
    Input("color_ADAMW","value"),
    Input("color_RADAM","value"),
    Input("color_RMSprop","value"),
    Input("color_sgd","value"),


    ])
           
    def update_graph(x_name,y_name,z_name,w_name,u_name, df_json, color_ADAM, color_ADAMW, color_RADAM, color_RMSprop, color_sgd):
        df_1 = pd.read_json(df_json)
        if u_name == "3d_symbol":
            fig = px.scatter_3d(df_1, x= x_name, y=y_name,z= z_name,symbol="algorithm", color=w_name,hover_data=['file_name','index'],width=1280,height=720)
        elif u_name == "3d_size":
            fig = px.scatter_3d(df_1, x= x_name, y=y_name,z= z_name,color="algorithm", color_discrete_sequence=[color_ADAMW, color_RADAM, color_RMSprop, color_sgd, color_ADAM], size=w_name,hover_data=['file_name','index'],width=1280,height=720, )
        elif u_name == "subplot":
            fig = px.scatter(df_1,x=x_name,y=y_name,facet_col="algorithm",size=z_name,color=w_name,hover_data=['file_name','index'],width=1280,height=720)
        elif u_name == "animated_subplot":
            fig = px.scatter(df_1, x=x_name, y=y_name,facet_col="algorithm",size=z_name,color=w_name,animation_frame="index", animation_group="algorithm", hover_data=["file_name","index"],width=1280,height=720)
            fig.update_layout(margin=dict(l=20,r=20,t=20,b=20))
            fig.update_xaxes(range=[-2,2])
            fig.update_yaxes(range=[-2,2])
            

        fig.update_layout(legend=dict(yanchor="top", y=1,xanchor="right",x=1, orientation="h"))
        fig.update_layout(clickmode='event+select')

        
        
        return fig

    @app.callback(
    Output('click-data','children'),
    [Input('desenho','clickData')]
    )
    
    
    def display_click_data(clickData):
        x = clickData
        y = clickData.get("points")[0]
        z = y.get("customdata")
        return json.dumps(z)
    

    
      
