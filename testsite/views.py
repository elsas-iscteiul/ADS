from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os, glob, shutil
from pathlib import Path
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

pattern = ''
sepa = ''
every_data = []

def index(request):
    fs = FileSystemStorage()
    global sepa
    global pattern

    x =[1,2,3]
    y =[1,2,3]

    fig = figure(plot_width=400, plot_height=400)
    fig.circle(x=x, y=y)
    script, div = components(fig)

    if request.method == "POST":
        files = request.FILES.getlist('myfiles')
        for f in files:
            fs.save(f._name, f)

        pattern = request.POST.get('pattern')
        sepa = request.POST.get('sep')

        csv_files = get_files()
        context = {'csv_files': csv_files, 'script':script,'div':div}
        populate()
        df = pd.DataFrame(every_data, columns=['accuracy','loss','val_accuracy','val_loss','file_name','index','algorithm'])
        print(df.loc[0,:])
        shutil.rmtree(settings.MEDIA_ROOT)

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


