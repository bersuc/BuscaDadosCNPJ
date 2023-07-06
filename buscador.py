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
        """
        Open lista.txt with all CNPJ's in each line. Ex: 
        27.865.757/0001-02
        27.865.757/0001-02

        Returns:
        List
        """
        self.arq = open('lista.txt', 'r')
        lines = [line.rstrip('\n') for line in self.arq]
        self.textao = open('dados.txt', 'w', encoding='utf-8')
        self.errosCNPJ = open('erros.txt', 'w')
        return lines

    def fechar(self):
        '''Close all files.'''
        self.arq.close()
        self.textao.close()
        self.errosCNPJ.close()
        print('Arquivos fechados com sucesso!')

    def gravaErros(self, cnpj):
        dados = {
            "Nome": "Erro ao buscar nome",
            "Atividade": "Erro ao buscar atividade",
            "CNAE": "Erro ao buscar CNAE"
        }
        self.errosCNPJ.write('CNPJ ' + cnpj)

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
                self.gravaErros(dados)
        else:
            print('Aguardando 5 segundos. Motivo Status Code não é 200: {}'
                  .format(sc))
            self.descansa()
        print(dados)
        return dados

    def gravaDados(self, cnpj, infocnpj):
        _nome = infocnpj['Nome']
        _atividade = infocnpj['Atividade']
        _cnae = infocnpj['CNAE']
        self.textao.write(cnpj + ';' + _nome + ';' +
                          _atividade + ';' + _cnae + '\n')

    def sanitize(self, line):
        """
               Sanitize the cnpj
               call the pegaJson function for each cnpj
               close the file
               """
        newLine = line.replace('.', '')
        newLine = newLine.replace('/', '')
        newLine = newLine.replace('-', '')
        return newLine

    def descansa(self):
        """Resting to not get blocked by API"""
        print('Ativando Descanso de 20 segundos')
        time.sleep(20)


if __name__ == "__main__":
    buscador = Buscador()
    inicio = time.time()
    lista = buscador.arquivos()

    for cnpj in lista:
        cnpj = buscador.sanitize(cnpj)
        infoCnpj = buscador.pegaJson(cnpj)
        buscador.gravaDados(cnpj, infoCnpj)
        buscador.descansa()

    buscador.fechar()
    fim = time.time()
    print(fim - inicio)
    print(infoCnpj)
