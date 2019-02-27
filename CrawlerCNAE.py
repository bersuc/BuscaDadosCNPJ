#!/usr/bin/python3
__author__ = 'Diogo Bersuc'

import json
import requests
import time

"""
Melhorando o arquivo
criando variavel global para chamar e fechar o arquivo de texto.
trabalhando corretamente OOP (ou tentando 😜)
"""

arq = None
textao = None
errosCNPJ = None
todos = None


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
    url = "https://www.receitaws.com.br/v1/cnpj/" + cnpj
    response = requests.get(url)
    sc = response.status_code
    if sc == 200:
        print('Status code: {}\nHorário: {}'.format(response.status_code, time.ctime()))
        todos = json.loads(response.text)
        # adicionando um try pois pode não existir o CNPJ
        try:
            dados = {
            "Nome": todos['nome'],
            "Atividade": todos['atividade_principal'][0]['text'],
            "CNAE": todos['atividade_principal'][0]['code']
            }
        except:
            # chamar log de erro para gravar CNPJ
            print('############################################\n')
            print('Erro ao obrter informações do {}\n'.format(cnpj))
            print('############################################\n')
            gravaErros(cnpj)
            dados = {
                "Nome": "Erro ao buscar nome",
                "Atividade": "Erro ao buscar atividade",
                "CNAE": "Erro ao buscar CNAE"
            }
        return dados
    else:
        print('Aguardando 5 segundos. Motivo Status Code não é 200: {}'.format(sc))
        time.sleep(5)
        pegaJson(cnpj)


"""
Tempo de 20 segundos para ler a API, só pode consultar 3x por minuto,
ou seja, 1 consulta a cada 20 segundos
"""
def descansa():
    time.sleep(20)


def gravaDados(cnpj, infocnpj):
    global textao
    _nome = infocnpj['Nome']
    _atividade = infocnpj['Atividade']
    _cnae = infocnpj['CNAE']
    textao.write(cnpj + ';' + _nome + ';' + _atividade + ';' + _cnae + '\n')


def gravaErros(cnpj):
    global errosCNPJ
    errosCNPJ.write('CNPJ ' + cnpj)


if __name__ == '__main__':
    lista = arquivos()
    a = 1
    for linha in lista:
        if len(linha) == 14:
            print("Fazendo o # {} de um total {}".format(a, len(lista)))
            print('CNPJ: ' + linha)
            infocnpj = pegaJson(linha)
            print(infocnpj['Nome'])
            print(infocnpj['Atividade'])
            print(infocnpj['CNAE'])
            print('\n')
            gravaDados(linha,infocnpj)
            if a != len(lista):
                descansa()
        else:
            pass
        a += 1
    fechar()