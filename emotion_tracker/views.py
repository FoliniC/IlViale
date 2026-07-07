from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .forms import EmotionIdentificationForm, PersonalNotesForm
from .models import EmotionIdentification    
import json


def analyze_emotion(form_data):
    """
    Analizza le risposte e identifica le emozioni.
    Questa è la stessa logica dell'app React, adattata per Python.
    """
    results = []
    
    energy = form_data.get('energy_type', '')
    triggers = form_data.get('triggers', [])
    impulses = form_data.get('impulses', [])
    valence = form_data.get('valence', '')
    body = form_data.get('body_sensations', [])
    intensity = int(form_data.get('intensity', 5))
    
    # Frustrazione
    if energy == 'blocked' or 'blocked' in impulses or \
       ('obstacle' in triggers and 'solve' in impulses):
        results.append({
            'emotion': 'Frustrazione',
            'confidence': 'Alta',
            'description': 'Sensazione di essere bloccato tra il voler fare qualcosa e non riuscirci. Nasce quando ci sono ostacoli che impediscono di raggiungere un obiettivo.',
            'suggestions': 'Prova a suddividere il compito in passi più piccoli. Identifica cosa ti blocca realmente e se puoi chiedere aiuto.'
        })
    
    # Rabbia
    if 'injustice' in triggers or 'attack' in impulses or \
       (energy == 'outward' and valence == 'negative'):
        results.append({
            'emotion': 'Rabbia',
            'confidence': 'Alta' if intensity > 6 else 'Media',
            'description': 'Reazione a qualcosa percepito come ingiusto, sbagliato o come ostacolo. Ti dà energia per cambiare la situazione.',
            'suggestions': 'Identifica cosa specificamente ti fa arrabbiare. Valuta se puoi agire costruttivamente sulla situazione.'
        })
    
    # Ansia/Paura
    if 'threat' in triggers or 'escape' in impulses or \
       'chest' in body or 'stomach' in body:
        results.append({
            'emotion': 'Ansia/Paura',
            'confidence': 'Media',
            'description': 'Risposta a una minaccia percepita, reale o immaginaria. Ti prepara a proteggerti.',
            'suggestions': 'Identifica se la minaccia è reale o anticipata. Le tecniche di respirazione possono aiutare a calmare la risposta fisica.'
        })
    
    # Tristezza
    if 'loss' in triggers or 'withdraw' in impulses or \
       (energy == 'low' and valence == 'negative'):
        results.append({
            'emotion': 'Tristezza',
            'confidence': 'Media',
            'description': 'Risposta a una perdita, mancanza o delusione. Segnala il bisogno di elaborare e di prendersi cura di sé.',
            'suggestions': 'Concediti tempo per elaborare. Parlarne con qualcuno di fiducia può aiutare.'
        })
    
    # Senso di colpa/Inadeguatezza
    if 'mistake' in triggers or ('withdraw' in impulses and 'mistake' in triggers):
        results.append({
            'emotion': 'Senso di colpa/Inadeguatezza',
            'confidence': 'Alta',
            'description': 'Sensazione di non essere all\'altezza o di aver fatto qualcosa di sbagliato. Può essere costruttivo o paralizzante.',
            'suggestions': 'Distingui tra colpa costruttiva (che ti aiuta a migliorare) e colpa eccessiva. Sii compassionevole con te stesso.'
        })
    
    # Stress/Sovraccarico
    if 'whole_body' in body or 'head' in body or 'weeks' in form_data.get('duration', ''):
        results.append({
            'emotion': 'Stress/Sovraccarico',
            'confidence': 'Alta',
            'description': 'Stato di tensione prolungata dovuto a troppe richieste o pressioni. Il corpo e la mente sono sotto sforzo.',
            'suggestions': 'È importante dare priorità al riposo. Valuta cosa puoi delegare o rimandare.'
        })
    
    # Gratitudine
    if 'benefit' in triggers and valence == 'positive':
        results.append({
            'emotion': 'Gratitudine',
            'confidence': 'Alta',
            'description': 'Riconoscimento e apprezzamento per qualcosa di positivo ricevuto. Rafforza le relazioni.',
            'suggestions': 'Esprimi la tua gratitudine alla persona. Anche un piccolo gesto ha grande valore.'
        })
    
    # Gioia/Contentezza
    if 'pleasant' in triggers and valence == 'positive' and 'approach' in impulses:
        results.append({
            'emotion': 'Gioia/Contentezza',
            'confidence': 'Alta',
            'description': 'Sensazione di piacere e benessere. Può variare da contentezza leggera a euforia.',
            'suggestions': 'Goditi questo momento! Condividerlo con altri può amplificare la sensazione.'
        })
    
    # Ambivalenza
    if valence == 'neutral' or (len(impulses) > 2 and 'avoid' in impulses):
        results.append({
            'emotion': 'Ambivalenza/Conflitto interno',
            'confidence': 'Media',
            'description': 'Presenza contemporanea di sentimenti contrastanti verso la stessa situazione. È normale e umano.',
            'suggestions': 'Riconosci entrambe le parti. Non devi scegliere subito, puoi convivere con l\'incertezza per un po\'.'
        })
    
    if not results:
        results.append({
            'emotion': 'Emozione complessa o mista',
            'confidence': 'Bassa',
            'description': 'Le tue risposte indicano una situazione emotiva sfumata o particolare. Potrebbe essere utile esplorare ulteriormente.',
            'suggestions': 'Prova a scrivere liberamente dei tuoi sentimenti o parlane con qualcuno.'
        })
    
    return results


@login_required
def identifier_view(request):
    """Vista principale per l'identificatore di emozioni"""
    
    if request.method == 'POST':
        form = EmotionIdentificationForm(request.POST)
        
        if form.is_valid():
            # Prepara i dati per l'analisi
            form_data = {
                'energy_type': form.cleaned_data['energy_type'],
                'triggers': form.cleaned_data['triggers'],
                'impulses': form.cleaned_data['impulses'],
                'valence': form.cleaned_data['valence'],
                'body_sensations': form.cleaned_data['body_sensations'],
                'intensity': form.cleaned_data['intensity'],
                'duration': form.cleaned_data['duration'],
            }
            
            # Analizza le emozioni
            identified_emotions = analyze_emotion(form_data)
            
            # Salva nel database
            identification = EmotionIdentification.objects.create(
                user=request.user,
                situation=form.cleaned_data['situation'],
                body_sensations=form.cleaned_data['body_sensations'],
                energy_type=form.cleaned_data['energy_type'],
                triggers=form.cleaned_data['triggers'],
                impulses=form.cleaned_data['impulses'],
                intensity=form.cleaned_data['intensity'],
                valence=form.cleaned_data['valence'],
                duration=form.cleaned_data['duration'],
                identified_emotions=identified_emotions
            )
            
            messages.success(request, 'Identificazione salvata con successo!')
            return redirect('emotion_tracker:detail', pk=identification.pk)
    else:
        form = EmotionIdentificationForm()
    
    return render(request, 'emotion_tracker/identifier.html', {'form': form})


@login_required
def history_view(request):
    """Vista per visualizzare lo storico delle identificazioni"""
    
    identifications = EmotionIdentification.objects.filter(user=request.user)
    
    # Filtri opzionali
    emotion_filter = request.GET.get('emotion')
    if emotion_filter:
        # Filtra per emozione primaria
        identifications = [
            i for i in identifications 
            if i.get_primary_emotion().lower() == emotion_filter.lower()
        ]
    
    return render(request, 'emotion_tracker/history.html', {
        'identifications': identifications
    })


@login_required
def detail_view(request, pk):
    """Vista dettaglio di una singola identificazione"""
    
    identification = get_object_or_404(
        EmotionIdentification, 
        pk=pk, 
        user=request.user
    )
    
    if request.method == 'POST':
        notes_form = PersonalNotesForm(request.POST, instance=identification)
        if notes_form.is_valid():
            notes_form.save()
            messages.success(request, 'Note aggiornate!')
            return redirect('emotion_tracker:detail', pk=pk)
    else:
        notes_form = PersonalNotesForm(instance=identification)
    
    return render(request, 'emotion_tracker/detail.html', {
        'identification': identification,
        'notes_form': notes_form
    })


@login_required
@require_http_methods(["DELETE"])
def delete_view(request, pk):
    """Vista per eliminare un'identificazione"""
    
    identification = get_object_or_404(
        EmotionIdentification, 
        pk=pk, 
        user=request.user
    )
    identification.delete()
    
    return JsonResponse({'status': 'success'})
