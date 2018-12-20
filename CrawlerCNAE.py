import json
import requests
import time

#abre o arquivo com os CNPJ's por linha
arq = open('lista.txt','r')

#entende que a quebra de linha corresponde a 1 cnpj
lines = [line.rstrip('\n') for line in arq]

#cria o arquivo onde serão inseridos os dados coletados
textao = open('dados.txt','w')

#cria o arquivo de log para ler os CNPJ's com problemas
errosCNPJ = open('erros.txt','w')

#numero da linha que esta sendo percorrida
a = 1

for i in lines:

    if len(i) <14:
        pass
    else:
        print("\nFazendo o # {} de um total {}".format(a, lines.__len__()))
        url1 = "https://www.receitaws.com.br/v1/cnpj/" + i
        
        response = requests.get(url1)
        sc = response.status_code

        #Se o status code da pag for 200, segue o loop
        if sc == 200:      
            print('Status code: {}\nHorário: {}'.format(response.status_code,time.ctime()))
            todos = json.loads(response.text)
            #pega o nome no JSON e imprime para verificar na tela se há erro
            if 'nome' in todos:
                nome = todos['nome']
                atividade = todos['atividade_principal'][0]['text']
                cnae = todos['atividade_principal'][0]['code']

                #tamanho da atividade
                tamanhoAtividade = len(atividade)

                #formatando a exibição para ficar mais limpa
                print(tamanhoAtividade * '-')
                print(i)
                print(nome)
                print(atividade)
                print(cnae)
                print(tamanhoAtividade * '-')

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