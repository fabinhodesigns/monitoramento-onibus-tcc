from django.shortcuts import render
from .models import Onibus, Parada

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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


HERE_API_KEY = "nchTlZMEpb97sB_zT9jZRhPUP5jQZpczxEoPg27Jxrw"

# Variáveis para armazenar localizações em tempo real
localizacao_usuario = {"latitude": None, "longitude": None}
localizacao_onibus = {"latitude": None, "longitude": None}

@csrf_exempt
def atualizar_localizacao_usuario(request):
    global localizacao_usuario
    if request.method == 'POST':
        dados = json.loads(request.body)
        localizacao_usuario["latitude"] = dados.get("latitude")
        localizacao_usuario["longitude"] = dados.get("longitude")
        return JsonResponse({"status": "Localização do usuário atualizada!"})
    return JsonResponse({"erro": "Método não permitido"}, status=405)

@csrf_exempt
def atualizar_localizacao_onibus(request):
    global localizacao_onibus
    if request.method == 'POST':
        dados = json.loads(request.body)
        localizacao_onibus["latitude"] = dados.get("latitude")
        localizacao_onibus["longitude"] = dados.get("longitude")
        return JsonResponse({"status": "Localização do ônibus atualizada!"})
    return JsonResponse({"erro": "Método não permitido"}, status=405)

def calcular_tempo_chegada(request):
    global localizacao_usuario, localizacao_onibus

    # Buscar localização fixa da parada no banco
    parada = Parada.objects.first()
    if not parada:
        return JsonResponse({"erro": "Parada não encontrada"}, status=400)

    if None in localizacao_usuario.values() or None in localizacao_onibus.values():
        return JsonResponse({"erro": "Localizações do usuário ou ônibus não definidas!"}, status=400)

    # Consultar tempo estimado do usuário até a parada
    url_usuario = f"https://router.hereapi.com/v8/routes?transportMode=pedestrian&origin={localizacao_usuario['latitude']},{localizacao_usuario['longitude']}&destination={parada.latitude},{parada.longitude}&return=summary&apikey={HERE_API_KEY}"
    resposta_usuario = requests.get(url_usuario).json()

    # Consultar tempo estimado do ônibus até a parada
    url_onibus = f"https://router.hereapi.com/v8/routes?transportMode=bus&origin={localizacao_onibus['latitude']},{localizacao_onibus['longitude']}&destination={parada.latitude},{parada.longitude}&return=summary&apikey={HERE_API_KEY}"
    resposta_onibus = requests.get(url_onibus).json()

    try:
        tempo_usuario = resposta_usuario["routes"][0]["sections"][0]["summary"]["duration"] // 60  # Convertendo para minutos
        tempo_onibus = resposta_onibus["routes"][0]["sections"][0]["summary"]["duration"] // 60  # Convertendo para minutos

        # Comparação dos tempos
        diferenca = tempo_onibus - tempo_usuario
        if diferenca > 2:
            status = "Você tem tempo suficiente para pegar o ônibus."
        elif -2 <= diferenca <= 2:
            status = "Corra! O ônibus está quase chegando."
        else:
            status = "Você já perdeu o ônibus."

        return JsonResponse({
            "tempo_usuario": tempo_usuario,
            "tempo_onibus": tempo_onibus,
            "status": status
        })

    except (KeyError, IndexError):
        return JsonResponse({"erro": "Erro ao obter tempo estimado!"}, status=500)