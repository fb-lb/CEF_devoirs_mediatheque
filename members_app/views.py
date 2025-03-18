from django.shortcuts import render

def mediapage(request):
    return render(request, 'media.html')