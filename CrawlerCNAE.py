import json
import requests
import time


arq = open('lista.txt','r')
lines = [line.rstrip('\n') for line in arq]
textao = open('dados.txt','w')
errosCNPJ = open('erros.txt','w')

#numero da linha que esta sendo percorrida
a = 1

for i in lines:

    if len(i) <14:
        pass
    else:
        print("Fazendo o # {} de um total {}".format(a, lines.__len__()))
        url1 = "https://www.receitaws.com.br/v1/cnpj/" + i
        
        response = requests.get(url1)
        sc = response.status_code

        #Se o status code da pag for 200, segue o loop
        if sc == 200:      
            print('\nStatus code: {}\nHorário: {}'.format(response.status_code,time.ctime()))
            todos = json.loads(response.text)
            #pega o nome no JSON e imprime para verificar na tela se há erro
            if 'nome' in todos:
                nome = todos['nome']
                print('\n')
                print(i)
                print(nome)
                        
                #pega a atividade index 0 e dentro dela o text (tipo de atividade) no JSON 
                atividade = todos['atividade_principal'][0]['text']
                # imprime para verificar na tela se há erro
                print(atividade)

                #pega a atividade index 0 e dentro dela o CNAE (código de atividade) no JSON 
                cnae = todos['atividade_principal'][0]['code']
                # imprime para verificar na tela se há erro
                print(cnae + "\n")

                #joga no arquivo as informações obtidas do cnpj
                textao.write('{}; {}; {}; {}'.format(i,nome,atividade,cnae))
                textao.write('\n')
            else:
                print('############################################\n')
                print('Erro ao obrter informações do {}\n'.format(i))
                print('############################################\n')
                errosCNPJ.write('-> Erro : CNPJ {}'.format(i))
                errosCNPJ.write('\n')

        # Aguarda 20 segs para dar o loop
        # A API só permite 3 conexões por minuto (1 a cada 20 seg)
        a = a + 1
        if a!= lines.__len__:
            time.sleep(20)
        

textao.close()
print("""Finalizado com sucesso! Parabéns!!! """)