from django.shortcuts import redirect, render

def biblioteca_redirect(request):
    return redirect('https://mailchi.mp/e4fc2f1a5400/ellida')

def biblioteca_iframe(request):
    return render(request, 'biblioteca/iframe.html')
