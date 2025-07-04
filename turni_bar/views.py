from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Gruppo, Barista, Turno

@login_required
def home(request):
    gruppi = Gruppo.objects.filter(creato_da=request.user)
    return render(request, 'turni_bar/lista_gruppi.html', {'gruppi': gruppi})

@login_required
def gestione_turni(request, gruppo_id):
    gruppo = get_object_or_404(Gruppo, id=gruppo_id, creato_da=request.user)
    baristi = gruppo.barista_set.all().order_by('turni_effettuati')
    
    if request.method == 'POST':
        barista_id = request.POST.get('barista')
        barista = get_object_or_404(Barista, id=barista_id, gruppo=gruppo)
        
        # Registra il turno
        Turno.objects.create(barista=barista)
        
        # Aggiorna il conteggio
        barista.turni_effettuati += 1
        barista.save()
        
        return redirect('gestione_turni', gruppo_id=gruppo.id)
    
    return render(request, 'turni_bar/gestione_turni.html', {
        'gruppo': gruppo,
        'baristi': baristi
    })

@login_required
def gestione_turni_no_id(request):
    gruppi = Gruppo.objects.filter(creato_da=request.user)
    baristi = Barista.objects.filter(gruppo__in=gruppi).order_by('turni_effettuati')
    
    if request.method == 'POST':
        barista_id = request.POST.get('barista')
        barista = get_object_or_404(Barista, id=barista_id, gruppo__in=gruppi)
        
        # Registra il turno
        Turno.objects.create(barista=barista)
        
        # Aggiorna il conteggio
        barista.turni_effettuati += 1
        barista.save()
        
        return redirect('gestione_turni_no_id')
    
    return render(request, 'turni_bar/gestione_turni.html', {
        'gruppi': gruppi,
        'baristi': baristi
    })

@login_required
def lista_gruppi(request):
    gruppi = Gruppo.objects.filter(creato_da=request.user)
    return render(request, 'turni_bar/lista_gruppi.html', {'gruppi': gruppi})