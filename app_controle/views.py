from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import PessoaForm
from .models import Pessoa, Funcionario

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


def pesquisar_funcionario(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        try:
            pessoa = Pessoa.objects.get(cpf=cpf)
            return redirect('funcionarios/cadastrar_funcionario.html', cpf=pessoa.cpf)  # Redireciona para cadastrar_funcionario.html
        except Pessoa.DoesNotExist:
            return redirect('pessoas/cadastro_pessoa')  # Redireciona para pesquisar_funcionario.html
    return render(request, 'funcionarios/pesquisar_funcionario.html')


def cadastrar_funcionario(request, cpf):
    pessoa = get_object_or_404(Pessoa, cpf=cpf)  # Busca a pessoa pelo CPF

    if request.method == 'POST':
        data_admissao = request.POST.get('data_admissao')
        funcao = request.POST.get('funcao')

        # Cria uma nova instância de Funcionario
        funcionario = Funcionario(
            pessoa=pessoa,
            data_admissao=data_admissao,
            funcao=funcao,
        )
        funcionario.save()
        return redirect('home')  # Redireciona para a página inicial após o cadastro

    return render(request, 'funcionarios/cadastrar_funcionario.html', {'pessoa': pessoa})