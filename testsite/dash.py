import dash, glob, shutil
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from django.conf import settings
from django_plotly_dash import DjangoDash
from plotly.subplots import make_subplots
import plotly.graph_objects as go

every_data = []

def get_files(pattern):
    files = []
    for f in glob.glob(settings.MEDIA_ROOT + "/" + pattern):
        files.append(f)

    return files

def populate(pattern, sep):
    global every_data
    files = get_files(pattern)
    for f in files:
        name = f.split("/")[-1]
        algorithm = name.split("_")[0]
        df = pd.read_csv(f,sep=sep)
        for index, row in df.iterrows():
            aux = [row['accuracy'],row['loss'],row['val_accuracy'],row['val_loss'],name,index,algorithm]
            every_data.append(aux)

populate("*_run*.csv",";")

app = DjangoDash('DashApp')


app.layout = html.Div([
    html.Label('Padrao de nome'),
    dcc.Input(id='pattern', type='text', value='*_run*.csv'),
    html.Label('Separador'),
    dcc.Input(id='sep', type='text', value=';'),
    html.Br(),
    html.Label('Algoritmos'),
    dcc.Dropdown(
        options=[
            {'label': 'ADAM','value':'ADAM'},
            {'label': 'ADAMW','value':'ADAMW'},
            {'label': 'RADAM','value':'RADAM'},
            {'label': 'RMSprop','value':'RMSProp'},
            {'label': 'SGD','value':'SGD'}
        ],
        multi = True
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
    
    html.Label('Gráfico'),
    dcc.Dropdown(
        id='u_type',
        options=[
            {'label':'3d_symbol', 'value':'3d_symbol'},
            {'label':'3d_size', 'value':'3d_size'},
            {'label':'subplot', 'value':'subplot'},
            
        ],
    ),
    dcc.Graph(id='desenho', config={'displayModeBar': False})
    
])

@app.callback(
    Output('desenho','figure'),
    [Input('x_type','value'),
    Input('y_type','value'),
    Input('z_type','value'),
    Input('w_type','value'),
    Input("u_type","value"),
    
    ])
def update_graph(x_name,y_name,z_name,w_name,u_name):
    global every_data
    df = pd.DataFrame(every_data, columns=['accuracy','loss','val_accuracy','val_loss','file_name','index','algorithm'])
    if u_name == "3d_symbol":
        fig = px.scatter_3d(df, x= x_name, y=y_name,z= z_name,symbol="algorithm", color=w_name,hover_data=['file_name','index'],width=1280 ,height=720)
    elif u_name == "3d_size":
        fig = px.scatter_3d(df, x= x_name, y=y_name,z= z_name,color="algorithm", size=w_name,hover_data=['file_name','index'],width=1280 ,height=720)
    elif u_name == "subplot":
        fig = px.scatter(df,x=x_name,y=y_name,symbol="algorithm",size=z_name,color=w_name,hover_data=['file_name','index'],width=1280 ,height=720)
        
    fig.update_layout(legend=dict(yanchor="top", y=0.99,xanchor="right",x=0.1, orientation="h"))
    return fig

