from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os


file_arr = []
fs = FileSystemStorage()

def index(request):
    if request.method == "POST":
        
        
        files = request.FILES.getlist("myfile")
        file_arr = files
        
        for file in file_arr:
            
            file_arr.append(file._name)
            
            fs.save(file._name, file)
            
        return render(request, "testsite/index.html", {
            
            "uploaded_file_url" : file_arr
        })
           
            
        
     
             
    return render(request, "testsite/index.html")


