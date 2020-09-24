# Sobre o sistema
O sistema consiste em uma busca por dados do CNPJ em uma API da ReceitaWS.

## Funcionamento
Para funcionar, você deve ter na mesma pasta o arquivo **lista.txt** com os sequintes requisitos:
* **Apenas** um CNPJ por linha
* Não importa se existem pontos ou qualquer outro caractere não numérico no sistema
* Possui um intervalo de 20 segundos entre cada consulta, para não ser bloqueada pela API
* Após rodar os dados, o arquivo **dados.txt** será gravado com as informações do CNPJ
* Caso não consiga capturar dados de um CNPJ, este CNPJ irá para o arquivo **erros.txt** para avaliação.
  
## Passo a Passo
* Rodar o arquivo CrawlerCNAE.py e aguardar.
* As informações de cada CNPJ também aparecerão na tela.
  

