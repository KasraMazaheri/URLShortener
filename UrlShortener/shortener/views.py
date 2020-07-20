from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from .models import URL
from .shrinker import shrink, AdminConfig


def home(request):
    return render(request, 'shortener/home.html')

def shorten(request):
    url = request.GET["url"]
    shortenedURL = shrink(url)
    try:
        URL.objects.get(shortenedURL = shortenedURL)
    except URL.DoesNotExist:
        _url = URL(targetURL = url, shortenedURL = shortenedURL)
        _url.save()
    return render(request, 'shortener/home.html', {
        'shortenedURL':shortenedURL
        })

def retrieve(request, inputURL):
    adminConfig = AdminConfig.objects.get(pk=1)
    
    inputURL = adminConfig.myDomain + inputURL
    target = get_object_or_404(URL, shortenedURL = inputURL)
    targetURL = target.targetURL
    if(targetURL[:4] != 'http'):
        targetURL = 'http://'+targetURL
    return redirect(targetURL)
