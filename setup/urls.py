from django.contrib import admin
from django.urls import path

from urna.views import UrnaHomeView

from urna.views import CandidatoListView
from urna.views import CandidatoCreateView
from urna.views import CandidatoUpdateView
from urna.views import CandidatoDeleteView

from urna.views import EleitorListView
from urna.views import EleitorCreateView
from urna.views import EleitorDeleteView

from urna.views import SecaoEleitoralView
from urna.views import VotacaoView
from urna.views import BuscarCandidatoView
from urna.views import ResultadoVotacaoView

urlpatterns = [
    # Rota default Django
    path('admin/', admin.site.urls),
    
    # Rota de Menu
    path("", UrnaHomeView.as_view(), name='urna_home'),
    
    # Rotas de candidatos
    path("candidatos", CandidatoListView.as_view(), name="candidato_list"),
    path("candidatos/create", CandidatoCreateView.as_view(), name="candidato_create"),
    path("candidatos/update/<int:pk>", CandidatoUpdateView.as_view(), name="candidato_update"),
    path("candidatos/delete/<int:pk>", CandidatoDeleteView.as_view(), name="candidato_delete"),
    
    # Rotas de eleitores
    path("eleitores", EleitorListView.as_view(), name="eleitor_list"),
    path("eleitores/create", EleitorCreateView.as_view(), name="eleitor_create"),
    path("eleitores/delete/<int:pk>", EleitorDeleteView.as_view(), name="eleitor_delete"),
    
    # Rotas de votação
    path("secaoEleitoral", SecaoEleitoralView.as_view(), name= "secao_eleitoral"),
    path("votacao/<str:tituloEleitor>", VotacaoView.as_view(), name="votacao"),
    path("candidatos/buscar", BuscarCandidatoView.as_view(), name="buscar_candidato"),
    path("resultado", ResultadoVotacaoView.as_view(), name="votacao_resultado")
]

