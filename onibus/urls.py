from django.contrib import admin
from django.urls import path
from monitoramento.views import home, atualizar_localizacao_usuario, atualizar_localizacao_onibus, calcular_tempo_chegada 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/atualizar_localizacao_usuario/', atualizar_localizacao_usuario, name='atualizar_localizacao_usuario'),
    path('api/atualizar_localizacao_onibus/', atualizar_localizacao_onibus, name='atualizar_localizacao_onibus'),
    path('api/calcular_tempo_chegada/', calcular_tempo_chegada, name='calcular_tempo_chegada'),
]
