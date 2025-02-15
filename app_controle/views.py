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

            # Se a pessoa já for um funcionário, redireciona e exibe um alerta
            if Funcionario.objects.filter(pessoa=pessoa).exists():
                messages.error(request, "Funcionário já cadastrado!")
                return redirect('pesquisar_funcionario')

            return redirect('cadastrar_funcionario', cpf=pessoa.cpf)
        except Pessoa.DoesNotExist:
            messages.error(request, "Pessoa não encontrada! Cadastre primeiro.")
            return redirect('cadastro_pessoa')

    return render(request, 'funcionarios/pesquisar_funcionario.html')


def cadastrar_funcionario(request, cpf):
    pessoa = get_object_or_404(Pessoa, cpf=cpf)

    # Verifica se a pessoa já é um funcionário
    if Funcionario.objects.filter(pessoa=pessoa).exists():
        messages.error(request, "Funcionário já cadastrado!")
        return redirect('pesquisar_funcionario')

    if request.method == 'POST':
        data_admissao = request.POST.get('data_admissao')
        funcao = request.POST.get('funcao')

        funcionario = Funcionario(
            pessoa=pessoa,
            data_admissao=data_admissao,
            funcao=funcao,
        )
        funcionario.save()
        messages.success(request, "Cadastro realizado com sucesso!")  # Mensagem de sucesso
        return redirect('home')

    return render(request, 'funcionarios/cadastrar_funcionario.html', {'pessoa': pessoa})
