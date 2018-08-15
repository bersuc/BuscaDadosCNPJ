import json
import requests
import time

arq = open('lista.txt','r')
lines = [line.rstrip('\n') for line in arq]
textao = open('dados.txt','w')
a = 1

for i in lines:
    print("Fazendo o # {} de um total {}".format(a, lines.__len__() -1 ))
    url1 = "https://www.receitaws.com.br/v1/cnpj/" + i
    response = requests.get(url1)
    sc = response.status_code
    if sc == 200:      
        print('\nStatus code: {}\nHorário: {}'.format(response.status_code,time.ctime()))
        todos = json.loads(response.text)
        fantasia = todos['nome']
        print(fantasia)
        emails = todos['email']
        print(emails + "\n")
        textao.write('{},{}'.format(fantasia,emails))
        #aguarda 20 segs
        time.sleep(20)
        a = a + 1


