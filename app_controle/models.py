from django.db import models
from datetime import date

class Pessoa(models.Model):
    cpf = models.CharField(max_length=14, primary_key=True, unique=True, verbose_name="CPF")
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    endereco = models.CharField(max_length=200, verbose_name="Endereço")
    numero = models.CharField(max_length=10, verbose_name="Número")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(max_length=50, verbose_name="Estado")
    pais = models.CharField(max_length=50, verbose_name="País")
    telefone = models.CharField(max_length=15, verbose_name="Telefone")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")

    def __str__(self):
        return f'CPF: {self.cpf}'

class Funcionario(models.Model):
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE, verbose_name="Pessoa")
    data_admissao = models.DateField(verbose_name="Data de Admissão")
    funcao = models.CharField(max_length=100, verbose_name="Funcao", default="Não informado")


    def __str__(self):
        return f'{self.pessoa.nome} - Cargo: {self.funcao}'



class EPI(models.Model):
    CATEGORIAS_CHOICES = [
        ('Proteção Auditiva', 'Proteção Auditiva'),
        ('Proteção Facial', 'Proteção Facial'),
        ('Proteção para os Pés', 'Proteção para os Pés'),
        ('Proteção contra Quedas', 'Proteção contra Quedas'),
        ('Proteção para as Mãos', 'Proteção para as Mãos'),
        ('Proteção Ocular', 'Proteção Ocular'),
        ('Proteção para Cabeça', 'Proteção para Cabeça'),
    ]

    codigo_barras = models.CharField(max_length=50, primary_key=True, verbose_name="Código de Barras")
    nome = models.CharField(max_length=100, verbose_name="Nome do EPI")
    categoria = models.CharField(max_length=50, choices=CATEGORIAS_CHOICES, verbose_name="Categoria")
    validade = models.DateField(null=True, blank=True, verbose_name="Data de Validade")
    fabricante = models.CharField(max_length=100, verbose_name="Fabricante")
    quantidade_disponivel = models.PositiveIntegerField(default=0, verbose_name="Quantidade Disponível")

    def __str__(self):
        return f"Produto: {self.nome} => Códgo de Barra: {self.codigo_barras} => Qtd: {self.quantidade_disponivel}"


class EntregaEpi(models.Model):
    documento = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name="Documento")
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, verbose_name="Funcionário")
    epi = models.ForeignKey(EPI, on_delete=models.CASCADE, verbose_name="EPI")
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade Entregue")
    data_entrega = models.DateField(default=date.today, verbose_name="Data de Entrega")

    def __str__(self):
        return f"Entrega de {self.funcionario.pessoa.nome} - CPF: {self.documento.cpf} - {self.epi.nome} (Qtd: {self.quantidade}) em {self.data_entrega}"


class DevolverEpi(models.Model):
    documento = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name="Documento")
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, verbose_name="Funcionário")
    epi = models.ForeignKey(EPI, on_delete=models.CASCADE, verbose_name="EPI")
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade Devolvida")
    data_devolucao = models.DateField(null=True, blank=True, verbose_name="Data de Devolução")

    def __str__(self):
        return f"Devolução de {self.funcionario.pessoa.nome} - CPF: {self.documento.cpf} - {self.epi.nome} (Qtd: {self.quantidade}) em {self.data_devolucao}"
