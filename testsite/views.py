from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os, glob, shutil
from pathlib import Path
import pandas as pd
from plotly.offline import plot
import plotly.express as px

pattern = ''
sepa = ''
every_data = []

def index(request):
    fs = FileSystemStorage()
    global sepa
    global pattern

    if request.method == "POST":
        files = request.FILES.getlist('myfiles')
        for f in files:
            fs.save(f._name, f)

        pattern = request.POST.get('pattern')
        sepa = request.POST.get('sep')

        populate()

        df = pd.DataFrame(every_data, columns=['accuracy','loss','val_accuracy','val_loss','file_name','index','algorithm'])
        shutil.rmtree(settings.MEDIA_ROOT)

        fig = px.scatter(df, x="accuracy",y="loss",color="algorithm",hover_name="algorithm",hover_data=["file_name","index"])
        
        div = plot(fig, output_type='div', include_plotlyjs=False)

        context = {'div': div}

        return render(request, "testsite/index.html", context)
    
    return render(request, "testsite/index.html")


def get_files():
    global pattern
    files = []
    for f in glob.glob(settings.MEDIA_ROOT + "/" + pattern):
        files.append(f)

    return files

def populate():
    global every_data
    global sepa
    files = get_files()
    for f in files:
        name = f.split("/")[-1]
        algorithm = name.split("_")[0]
        df = pd.read_csv(f,sep=sepa)
        for index, row in df.iterrows():
            aux = [row['accuracy'],row['loss'],row['val_accuracy'],row['val_loss'],name,index,algorithm]
            every_data.append(aux)


