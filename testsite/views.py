from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
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



        from . import dash 
        context = {'load': True}


        return render(request, "testsite/index.html", context)
    
    return render(request, "testsite/index.html")


