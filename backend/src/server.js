const express = require('express'); //importação do express
const app = express(); //criação do objeto chamado app com o express

app.use(express.json()); //Usando o json

//Criação da primeira rota de teste
app.get('/', (req, res) => {
    res.send('Hello World!');
});

//Subir em uma porta especifica, porta 3000 e a porta padrao do Express
app.listen(3000, () => {
    console.log('Listening on port 3000');
});
