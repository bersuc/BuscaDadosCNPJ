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
    while response.status_code != 200:
        repouso = 30 #em segundos
        print("Aguardando liberação do servidor... Testaremos de novo em {} segundos".format(repouso))
        time.sleep(repouso)
        response = requests.get(url1)
    print('Status code: {}\n Horário: {}'.format(response.status_code,time.ctime()))
    todos = json.loads(response.text)
    fantasia = todos['nome']
    print(fantasia)
    emails = todos['email']
    print(emails)
    textao.write('{},{}\n'.format(fantasia,emails))
    #aguarda 20 segs
    time.sleep(30)
    a = a + 1


