import json
import requests
import time

arq = open('lista.txt','r')
lines = [line.rstrip('\n') for line in arq]
textao = open('dados.txt','w')
a = 1

for i in lines:
    print("Fazendo o # {} de um total {}".format(a, lines.__len__()))
    url1 = "https://www.receitaws.com.br/v1/cnpj/" + i
    response = requests.get(url1)
    todos = json.loads(response.text)
    print('{} {}'.format(response,time.ctime()))
    fantasia = todos['nome']
    print(fantasia)
    emails = todos['email']
    print(emails)
    textao.write('{},{}\n'.format(fantasia,emails))
    #aguarda 20 segs
    time.sleep(20)
    a = a + 1



