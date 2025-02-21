from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro-pessoa/', views.cadastro_pessoa, name='cadastro_pessoa'),
    path('pesquisar-funcionario/', views.pesquisar_funcionario, name='pesquisar_funcionario'),
    path('cadastrar-funcionario/<str:cpf>/', views.cadastrar_funcionario, name='cadastrar_funcionario'),

    path('gerar-codigo/', views.gerar_codigo_barras_view, name='gerar_codigo_barras'),
    path('buscar-epi/', views.buscar_epi, name='buscar_epi'),
    path('cadastrar-epi/', views.cadastrar_epi, name='cadastrar_epi'),

    path('busca-pessoa/', views.verificar_funcionario_epi, name='verificar_funcionario_epi'),
    path('entrega/', views.registrar_entrega, name='registrar_entrega'),
    path('buscar-epis/', views.buscar_epis_para_devolucao, name='buscar_epis_para_devolucao'),
    path('registrar-devolucao/', views.registrar_devolucao, name='registrar_devolucao'),
    path('lista-de-epis-emprestados/', views.listar_epis_emprestados, name='listar_epis_emprestados'),
]
