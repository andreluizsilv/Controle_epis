import random

def gerar_codigo_barras():
    prefixo = "789"  # Prefixo Brasil
    numeros = "".join(str(random.randint(0, 9)) for _ in range(9))  # 9 dígitos aleatórios
    codigo_parcial = prefixo + numeros

    # Cálculo do dígito verificador EAN-13
    def calcular_digito_verificador(codigo):
        soma = sum(int(c) * (3 if i % 2 else 1) for i, c in enumerate(codigo))
        return (10 - (soma % 10)) % 10

    digito_verificador = calcular_digito_verificador(codigo_parcial)
    return codigo_parcial + str(digito_verificador)
