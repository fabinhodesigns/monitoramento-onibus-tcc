from django.shortcuts import render
from .models import Onibus, Parada

def home(request):
    # Buscar os dados cadastrados no banco de dados:
    onibus = Onibus.objects.first()
    parada = Parada.objects.first()

    # Passar os dados para o template HTML:
    contexto = {
        'onibus': onibus,
        'parada': parada,
    }

    # Renderizar a página HTML chamada home.html
    return render(request, 'home.html', contexto)
