from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro-pessoa', views.cadastro_pessoa, name='cadastro_pessoa'),
    path('pesquisar-funcionario', views.pesquisar_funcionario, name='pesquisar_funcionario'),
    path('cadastrar-funcionario/<str:cpf>/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('cadastrar/', views.cadastrar_epi, name='cadastrar_epi'),
    path('gerar-codigo/', views.gerar_codigo_barras_view, name='gerar_codigo_barras'),

    path('buscar/', views.buscar_epi, name='buscar_epi'),
]
