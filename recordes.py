# Lê e grava o ranking (top 5) em um arquivo de texto.

import os

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(PASTA, "recordes.txt")
QUANTIDADE = 5

def pegar_pontos(recorde):
    return recorde["pontos"]
def carregar_recordes():
    recordes = []
    if not os.path.exists(ARQUIVO):
        return recordes

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha == "":
                continue
            partes = linha.split(";")
            if len(partes) == 2 and partes[1].isdigit():
                recordes.append({"nome": partes[0], "pontos": int(partes[1])})

    recordes.sort(key=pegar_pontos, reverse=True)
    return recordes[:QUANTIDADE]
def eh_recorde(pontos):
    if pontos <= 0:
        return False
    recordes = carregar_recordes()
    if len(recordes) < QUANTIDADE:
        return True
    return pontos > recordes[-1]["pontos"]
def salvar_recorde(nome, pontos):
    nome = nome.replace(";", "").strip()
    if nome == "":
        nome = "Pombo"
    recordes = carregar_recordes()
    recordes.append({"nome": nome, "pontos": pontos})
    recordes.sort(key=pegar_pontos, reverse=True)
    recordes = recordes[:QUANTIDADE]
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        for recorde in recordes:
            arquivo.write(f"{recorde['nome']};{recorde['pontos']}\n")