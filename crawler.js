var request = require('request');
cnpj = "24310946000112";
// url = "https://www.receitaws.com.br/v1/cnpj/" + cnpj;
var url = require('./test69346856000110.json');

console.log(url);

function buscador(url){
    request(url, function(error, response, body){
        return body;
    })
};

buscador(url)