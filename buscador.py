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
        print('Processo concluído com sucesso!')

    def pegaJson(self, cnpj):
        self.contador
        url = "https://www.receitaws.com.br/v1/cnpj/" + cnpj
        response = requests.get(url)
        # sc = response.status_code
        todos = json.loads(response.text)
        return todos


if __name__ == "__main__":
    var = Buscador().pegaJson("27865757000102")
    print(var)
