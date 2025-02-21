from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import *
from .models import *
from .utils import gerar_codigo_barras

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


def cadastrar_epi(request):
    codigo_barras = request.GET.get('codigo_barras', '')

    if request.method == 'POST':
        form = EPIForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "EPI cadastrado com sucesso!")
            return redirect('buscar_epi')
    else:
        form = EPIForm(initial={'codigo_barras': codigo_barras})

    return render(request, 'epis/cadastrar_epi.html', {'form': form})


def atualizar_epi(request, epi_nome):
    epi = get_object_or_404(EPI, nome=epi_nome)

    if request.method == 'POST':
        form = EPIForm(request.POST, instance=epi)
        if form.is_valid():
            form.save()
            messages.success(request, f"EPI {epi.nome} atualizado com sucesso!")
            return redirect('buscar_epi')
    else:
        form = EPIForm(instance=epi)

    return render(request, 'epis/cadastrar_epi.html', {'form': form, 'epi': epi})

def buscar_epi(request):
    codigo_barras = request.GET.get('codigo_barras', '').strip()

    if codigo_barras:
        epi = EPI.objects.filter(codigo_barras=codigo_barras).first()
        if epi:
            # Se o EPI já existir, atualizar a quantidade disponível
            nova_quantidade = int(request.GET.get('nova_quantidade', 0))
            epi.quantidade_disponivel += nova_quantidade
            epi.save()
            messages.success(request, f"EPI {epi.nome} atualizado com sucesso!")
            return redirect('buscar_epi')
        else:
            # Se não existir, redireciona para o cadastro com o código preenchido
            return redirect('cadastrar_epi')

    return render(request, 'epis/buscar_epi.html')



def gerar_codigo_barras_view(request):
    codigo_barras = gerar_codigo_barras()  # Gera um código novo
    return render(request, 'epis/gerar_codigo.html', {'codigo_barras': codigo_barras})



def verificar_funcionario_epi(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf', '').strip().replace('.', '').replace('-', '')  # Remove formatação do CPF
        codigo_barras = request.POST.get('codigo_barras', '').strip()

        # Verifica se a Pessoa existe pelo CPF
        try:
            pessoa = get_object_or_404(Pessoa, cpf=cpf)
        except:
            messages.error(request, "Pessoa não encontrada! Cadastre primeiro.")
            return redirect('cadastro_pessoa')

        # Verifica se a Pessoa é um Funcionário
        try:
            funcionario = get_object_or_404(Funcionario, pessoa=pessoa)
        except:
            messages.error(request, "Funcionário não encontrado! Cadastre primeiro.")
            return redirect('cadastrar_funcionario', cpf=cpf)

        # Verifica se o EPI existe pelo código de barras
        try:
            epi = get_object_or_404(EPI, codigo_barras=codigo_barras)
        except:
            messages.error(request, "EPI não encontrado! Cadastre primeiro.")
            return redirect('cadastrar_epi')

        # Verifica se o EPI tem quantidade disponível
        if epi.quantidade_disponivel <= 0:
            messages.error(request, "EPI indisponível no momento.")
            return redirect('buscar_epi')

        # Se tudo estiver correto, renderiza a página de entrega com os dados do funcionário e EPI
        return render(request, 'devolucao_epis/registrar_entrega.html', {'funcionario': funcionario, 'epi': epi})

    return render(request, 'devolucao_epis/verificar_funcionario_epi.html')



def registrar_entrega(request):
    if request.method == 'POST':
        form = EntregaEpisForm(request.POST)
        if form.is_valid():
            entrega = form.save(commit=False)
            if entrega.epi.quantidade_disponivel > 0:
                entrega.save()
                entrega.epi.quantidade_disponivel -= 1
                entrega.epi.save()
                messages.success(request, "EPI entregue com sucesso!")
                return redirect('listar_epis_emprestados')
            else:
                messages.error(request, "EPI indisponível para entrega.")
    else:
        form = EntregaEpisForm()

    return render(request, 'devolucao_epis/registrar_entrega.html', {'form': form})


def buscar_epis_para_devolucao(request):
    cpf = request.GET.get('cpf', '')
    epis_emprestados = []

    if cpf:
        epis_emprestados = EntregaEpi.objects.filter(funcionario__pessoa__cpf=cpf)

    return render(request, 'devolucao_epis/buscar_epis.html', {'epis_emprestados': epis_emprestados, 'cpf': cpf})


def registrar_devolucao(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        epis_devolvidos_ids = request.POST.getlist('epis_devolvidos')

        if epis_devolvidos_ids:
            for epi_id in epis_devolvidos_ids:
                entrega = get_object_or_404(EntregaEpi, id=epi_id)

                # Criando o registro de devolução
                devolucao = DevolverEpi.objects.create(
                    documento=entrega.documento,
                    funcionario=entrega.funcionario,
                    epi=entrega.epi,
                    data_devolucao=date.today()
                )

                # Atualizando a quantidade disponível
                entrega.epi.quantidade_disponivel += 1
                entrega.epi.save()

                # Removendo a entrega original
                entrega.delete()

            messages.success(request, "EPI(s) devolvido(s) com sucesso!")

        return redirect('buscar_epis_para_devolucao')

    return redirect('home')


def listar_epis_emprestados(request):
    # Pegamos todos os IDs de EPIs que já foram devolvidos
    epis_devolvidos = DevolverEpi.objects.values_list('epi_id', flat=True)
    # Filtramos os EPIs entregues que ainda não estão na lista dos devolvidos
    epis_emprestados = EntregaEpi.objects.filter(epi_id__in=epis_devolvidos)
    return render(request, 'devolucao_epis/listar_epis_emprestados.html', {'emprestados': epis_emprestados})
