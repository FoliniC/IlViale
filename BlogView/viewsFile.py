# views.py
import os
from django.http import HttpResponse
from django.conf import settings

def list_directory(request, path=''):
    directory_path = os.path.join(settings.BASE_DIR, path)

    if not os.path.isdir(directory_path):
        return HttpResponse("Directory not found", status=404)

    files = os.listdir(directory_path)
    response = "<h2>Directory Listing</h2><ul>"
    for file in files:
        file_path = os.path.join(path, file)
        response += f'<li><a href="/{file_path}">{file}</a></li>'
    response += "</ul>"

    return HttpResponse(response)
