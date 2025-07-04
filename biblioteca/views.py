import requests
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup

def biblioteca_redirect(request):
    return redirect('https://mailchi.mp/e4fc2f1a5400/ellida')

def biblioteca_iframe(request):
    url = "https://mailchi.mp/e4fc2f1a5400/ellida"
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    wrapper = soup.find("div", class_="wrapper")
    if wrapper:
        # Rimuovi tutte le intestazioni e hr SOLO nel primo wrapper
        for sel in [".ellida-title", ".ellida-subtitle", ".ellida-desc", "hr"]:
            tag = wrapper.select_one(sel)
            if tag:
                tag.decompose()
        # Se c'è un wrapper annidato, usa il suo contenuto
        inner_wrapper = wrapper.find("div", class_="wrapper")
        if inner_wrapper:
            content = inner_wrapper
        else:
            content = wrapper

        # Elimina il primo div con class mcnTextBlock sotto bodyContainer contentContainer
        body_container = content.find("div", class_="bodyContainer contentContainer")
        if body_container:
            mcn_textblock = body_container.find("div", class_="mcnTextBlock")
            if mcn_textblock:
                mcn_textblock.decompose()

        # Sostituisci "Dona su ProValtellina" con il link mantenendo lo stile originale
        for text in content.find_all(string="Dona su ProValtellina"):
            a_tag = soup.new_tag("a", href="/Biblioteca/dona/")
            a_tag.string = "Dona su ProValtellina"
            a_tag['style'] = (
                "background: #228;color: #fff;text-decoration: none;padding: 4px 16px;"
                "margin-top: 16px;display: inline-block;border-radius: 16px;"
                "-webkit-box-sizing: border-box;-moz-box-sizing: border-box;"
                "font-weight: normal;box-sizing: border-box !important;"
            )
            text.replace_with(a_tag)



        contenuto = str(content)
    else:
        # fallback: solo sostituzione testo
        contenuto = html.replace(
            "Dona su ProValtellina",
            '<a href="/Biblioteca/dona/">Dona su ProValtellina2</a>'
        )

    return render(request, "biblioteca/iframe.html", {"mailchimp_html": mark_safe(contenuto)})

def biblioteca_dona(request):
    return render(request, 'biblioteca/dona.html')
