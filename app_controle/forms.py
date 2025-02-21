from django import forms
from .models import *
from .utils import gerar_codigo_barras


class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class EPIForm(forms.ModelForm):
    class Meta:
        model = EPI
        fields = ['codigo_barras', 'nome', 'categoria', 'validade', 'fabricante', 'quantidade_disponivel']
        widgets = {
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'validade': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fabricante': forms.TextInput(attrs={'class': 'form-control'}),
            'quantidade_disponivel': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class EntregaEpisForm(forms.ModelForm):
    class Meta:
        model = EntregaEpi
        fields = ['documento', 'funcionario', 'epi', 'quantidade', 'data_entrega']
        widgets = {
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'data_entrega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class DevolucaoEpisForm(forms.ModelForm):
    class Meta:
        model = DevolverEpi
        fields = ['documento', 'funcionario', 'epi', 'quantidade', 'data_devolucao']
        widgets = {
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'data_devolucao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
