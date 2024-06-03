def ler_arquivo_entrada(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()
    modelo_origem = linhas[0].strip().strip(';')
    regras = [linha.strip() for linha in linhas[1:] if linha.strip() and not linha.startswith(';')]
    return modelo_origem, regras

def escrever_arquivo_saida(caminho_arquivo, modelo_destino, regras):
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(f";{modelo_destino}\n")
        for regra in regras:
            arquivo.write(f"{regra}\n")

def converter_para_duplamente_infinita(regras):
    regras_convertidas = []
    simbolo_inicio = '#'
    for regra in regras:
        estado_atual, simbolo_atual, novo_simbolo, direcao, novo_estado = regra.split()
        if estado_atual == '0' and simbolo_atual == '':
            regras_convertidas.append(f"0  {simbolo_inicio} {simbolo_inicio} r inicia")
            regras_convertidas.append(f"inicia  {simbolo_atual} {simbolo_atual} l esquerda")
            regras_convertidas.append(f"esquerda  {simbolo_inicio} {simbolo_inicio} r 0")
        else:
            if direcao == 'l':
                regras_convertidas.append(f"{estado_atual}  {simbolo_inicio} {simbolo_inicio} r {estado_atual}_verifica")
                regras_convertidas.append(f"{estado_atual}_verifica  {simbolo_inicio} {simbolo_inicio} * {estado_atual}")
                regras_convertidas.append(f"{estado_atual} {simbolo_atual} {novo_simbolo} {direcao} {novo_estado}")
            else:
                regras_convertidas.append(f"{estado_atual} {simbolo_atual} {novo_simbolo} {direcao} {novo_estado}")
    return regras_convertidas

def converter_para_semi_infinita(regras):
    regras_convertidas = []
    simbolo_inicio = '#'
    simbolo_fim = '&'
    regras_convertidas.append(f"0  {simbolo_inicio} {simbolo_inicio} r shift")
    for regra in regras:
        estado_atual, simbolo_atual, novo_simbolo, direcao, novo_estado = regra.split()
        if direcao == 'l':
            regras_convertidas.append(f"{estado_atual}  {simbolo_inicio} {simbolo_inicio} r {estado_atual}_verifica")
            regras_convertidas.append(f"{estado_atual}_verifica  {simbolo_inicio} {simbolo_inicio} * {estado_atual}")
            regras_convertidas.append(f"{estado_atual} {simbolo_atual} {novo_simbolo} {direcao} {novo_estado}")
        elif direcao == 'r':
            regras_convertidas.append(f"{estado_atual}  {simbolo_fim} {simbolo_fim} l {estado_atual}_verifica")
            regras_convertidas.append(f"{estado_atual}_verifica  {simbolo_fim}  {simbolo_fim} * {estado_atual}")
            regras_convertidas.append(f"{estado_atual} {simbolo_atual} {novo_simbolo} {direcao} {novo_estado}")
    return regras_convertidas

def traduzir_modelo():
    caminho_entrada = 'input.in'
    caminho_saida = 'output.out'
    modelo_origem, regras = ler_arquivo_entrada(caminho_entrada)
    if modelo_origem == 'S':
        modelo_destino = 'I'
        regras_convertidas = converter_para_duplamente_infinita(regras)
    elif modelo_origem == 'I':
        modelo_destino = 'S'
        regras_convertidas = converter_para_semi_infinita(regras)
    else:
        raise ValueError("Modelo de origem inválido")
    escrever_arquivo_saida(caminho_saida, modelo_destino, regras_convertidas)

# Exemplos de uso:
traduzir_modelo()
