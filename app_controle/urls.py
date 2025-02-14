from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro-pessoa', views.cadastro_pessoa, name='cadastro_pessoa'),
]
