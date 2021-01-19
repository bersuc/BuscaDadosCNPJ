#!/usr/bin/python3
__author__ = 'Diogo Bersuc'

import json
import requests
import time


arq = None
textao = None
errosCNPJ = None
todos = None
contador = 0


def arquivos():
    global arq
    global textao
    global errosCNPJ
    arq = open('lista.txt', 'r')
    lines = [line.rstrip('\n') for line in arq]
    textao = open('dados.txt', 'w')
    errosCNPJ = open('erros.txt', 'w')
    return lines


"""
Fecha os arquivos abertos anteriormente
"""


def fechar():
    global arq
    global textao
    global errosCNPJ
    arq.close()
    textao.close()
    errosCNPJ.close()
    print('Processo concluído com sucesso!')


def pegaJson(cnpj):
    global contador
    url = "https://www.receitaws.com.br/v1/cnpj/" + cnpj
    response = requests.get(url)
    sc = response.status_code
    if sc == 200:
        print('Status code: {}\nHorário: {}'.format(
            response.status_code, time.ctime()))
        todos = json.loads(response.text)
        # adicionando um try pois pode não existir o CNPJ
        try:
            dados = {
                "Nome": todos['nome'],
                "Atividade": todos['atividade_principal'][0]['text'],
                "CNAE": todos['atividade_principal'][0]['code']
            }
        except ValueError:
            # chamar log de erro para gravar CNPJ
            print('############################################\n')
            print('Erro ao obrter informações do cnpj')
            print('############################################\n')
            gravaErros(cnpj)
    #
    # possivel update
    #
    # elif response.status_code == 504:
    #     descansa()
    #     contador += 1
    #     print('o contador é {}' .format(contador))
    #     if contador > 3:
    #         gravaErros(cnpj)
    #         pass
    #     pegaJson(cnpj)
    else:
        print('Aguardando 5 segundos. Motivo Status Code não é 200: {}'.format(sc))
        descansa()
        pegaJson(cnpj)
    return dados


"""
Tempo de 20 segundos para ler a API, só pode consultar 3x por minuto,
ou seja, 1 consulta a cada 20 segundos
"""


def descansa():
    print('Ativando Descanso de 20 segundos')
    time.sleep(20)


def gravaDados(cnpj, infocnpj):
    global textao
    _nome = infocnpj['Nome']
    _atividade = infocnpj['Atividade']
    _cnae = infocnpj['CNAE']
    textao.write(cnpj + ';' + _nome + ';' + _atividade + ';' + _cnae + '\n')


def gravaErros(cnpj):
    global errosCNPJ
    dados = {
        "Nome": "Erro ao buscar nome",
        "Atividade": "Erro ao buscar atividade",
        "CNAE": "Erro ao buscar CNAE"
    }
    errosCNPJ.write('CNPJ ' + cnpj)


"""
Recebe a linha com o CNPJ, o CNPJ poderá conter pontos ou / - Padrão é xxx.xxx.xxx/xxxx-xx
Remover -> . / - 
"""


def removeChars(linha):
    newLinha = linha.replace('.', '')
    newLinha = newLinha.replace('/', '')
    newLinha = newLinha.replace('-', '')
    # verifica se é CNPJ quando tem 0001 numa determinada posição
    # if (newLinha[-6:-2]) == '0001':
    #     # No Loop = better
    #     # newLinha = ('0' * (14 - len(newLinha)) + newLinha)
    while len(newLinha) < 14:
        # enquanto o CNPJ for menor que 14, insere zeros no começo do CNPJ
        newLinha = '0' + newLinha
    return newLinha


if __name__ == '__main__':
    lista = arquivos()
    a = 1
    for linha in lista:
        linha = removeChars(linha)
        if len(linha) == 14:
            print("Fazendo o # {} de um total {}".format(a, len(lista)))
            print('CNPJ: ' + linha)
            infocnpj = pegaJson(linha)
            print(infocnpj['Nome'])
            print(infocnpj['Atividade'])
            print(infocnpj['CNAE'])
            print('\n')
            gravaDados(linha, infocnpj)
            if a != len(lista):
                descansa()
        else:
            pass
        a += 1
        contador = 0
    fechar()
