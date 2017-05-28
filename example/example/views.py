from django.shortcuts import render, redirect
from django.http import Http404
import django_zips3

def index(request):
    # download = django_zips3.generate_url("/Nothing/POS2041")    
    # return redirect(download)
    return render(request, "example/index.html", {})

def download(request):
    if request.method != 'POST':
        return Http404
    
    download = django_zips3.generate_url(request.POST.get('prefix'))    
    return redirect(download)