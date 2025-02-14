from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PessoaForm

def home(request):
    return render(request, 'home.html')

def cadastro_pessoa(request):
    if request.method == "POST":
        form = PessoaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso!")  # Mensagem de sucesso
            return redirect('cadastro_pessoa')  # Redireciona para a mesma página, limpando o formulário
        else:
            messages.error(request, "Erro ao cadastrar. Verifique os dados.")
    else:
        form = PessoaForm()  # Inicializa o formulário vazio

    return render(request, 'pessoas/cadastro_pessoa.html', {'form': form})
