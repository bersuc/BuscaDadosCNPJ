#!/usr/bin/python3
__author__ = 'Diogo Bersuc'

import json
import requests
import time


class Buscador:
    def __init__(self):
        self.arq = None
        self.textao = None
        self.errosCNPJ = None
        self.todos = None
        self.contador = 0

    def arquivos(self):
        self.arq = open('lista.txt', 'r')
        lines = [line.rstrip('\n') for line in self.arq]
        self.textao = open('dados.txt', 'w')
        self.errosCNPJ = open('erros.txt', 'w')
        return lines

    """
    Fecha os arquivos abertos anteriormente
    """
    def fechar(self):
        self.arq.close()
        self.textao.close()
        self.errosCNPJ.close()
        print('Arquivos fechados com sucesso!')

    def pegaJson(self, cnpj):
        self.contador
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
                # gravaErros(cnpj)
        else:
            print('Aguardando 5 segundos. Motivo Status Code não é 200: {}'
                  .format(sc))
            # descansa()
            # pegaJson(cnpj)
        return dados


if __name__ == "__main__":
    inicio = time.time()
    var = Buscador().pegaJson("27865757000102")
    fim = time.time()
    print(fim - inicio)
    print(var)
