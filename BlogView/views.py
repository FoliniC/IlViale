import os

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


import feedparser

def index(request):
    post_id = ""
    base_url = None
    try: 
        server = os.environ["SERVER_TYPE"]
    except KeyError:  
        server = "PROD"
    if server != 'DEV':
        base_url = request.build_absolute_uri
    
    # return HttpResponse("Hello, world.")
    if request.GET.get("url"):
        url = request.GET["url"]         #Getting URL
        post_id = request.GET["post_id"]         #Getting URL
        myfeed = feedparser.parse(url) #Parsing XML data
    else:
        post_id = request.GET.get("post_id")
        myfeed = feedparser.parse('http://ilvialedellaformica.blogspot.com/feeds/posts/default')
    return render(request, "reader.html", {"feed" : myfeed,"post_id" : post_id,"base_url" : base_url,} )