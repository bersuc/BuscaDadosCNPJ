#!/usr/bin/python3
__author__ = 'Diogo Bersuc'

import json
import requests
import time


class Buscador:
    def __init__(self, arq, textao, errosCNPJ, todos, contador):
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

    if __name__ == "__main__":
        pass
