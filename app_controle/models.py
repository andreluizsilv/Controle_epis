from django.db import models

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
        return f'{self.nome} - CPF: {self.cpf}'

class Funcionario(models.Model):
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE, verbose_name="Pessoa")
    data_admissao = models.DateField(verbose_name="Data de Admissão")
    funcao = models.CharField(max_length=100, verbose_name="Funcao", default="Não informado")


    def __str__(self):
        return f'{self.pessoa.nome} - Cargo: {self.funcao}'
