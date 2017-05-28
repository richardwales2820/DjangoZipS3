from django.shortcuts import render, redirect
import django_zips3

def index(request):
    download = django_zips3.generate_zips3("/Nothing/POS2041")    
    return redirect(download)
    return render(request, "example/index.html", {})