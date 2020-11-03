A simple API that registers a user with a valid e-mail address on MongoDB.

Dependencies OS:
docker
docker-compose

Sergera
Desafio API Simples
Considerações Gerais

Sua solução deve ser simples de ser executada, seguindo as condições abaixo:

    Seu sistema deve estar encapsulado em container(s) Docker;
    Registre no arquivo SOLUTION.md a arquitetura do projeto e as ideias que gostaria de implementar se tivesse mais tempo e explique como você as faria.

O Problema

O seu desafio consiste em criar uma API que é capaz de registrar usuários e retornar a lista de todos os usuários cadastrados. Um usário consiste de um email e um nome.

Exemplo: Você pode cadastrar o usuário

    nome: Daniel, email: daniel@mail.com

A API

Você deve criar uma API HTTP com as seguintes interfaces:
POST /user:

Esse interface será chamada cada vez que um usuário querer ser cadastrado. Recebe o parâmetro nome e email como json no body.

    Exemplo de uso: $ curl -d '{"name": "daniel", "email": "daniel@mail.com"}' http://localhost:8080/register

A api devera retornar um 400 (Bad Request) em caso da falta de algum parâmetro ou em caso de email invalido.
GET /users:

Retorna todos os usuários como um json dentro da chave users

    Exemplo de uso: $ curl http://localhost:8080/users

Exemplo de retorno:

    {
        "users": [
            {
                "name": "daniel",
                "email": "daniel@mail.com"
            },
            {
                "name": "sergio",
                "email": "sergio@mail.com"
            }
        ]
    }

Requisitos
Inicialização

Devemos ser capazes de rodar sua aplicação e iniciar o serviço com os seguintes passos

make setup  # build da(s) imagem(ns) docker
make run    # inicializa aplicação

Devemos ser capazes de rodar os testes com o comando

make test

A aplicação deverá OBRIGATORIAMENTE funcionar com os comandos acima.
Avaliação

    Você deverá entregar seu código e uma documentação SOLUTION.md.
    Não tenha medo de usar bibliotecas e sistemas open sources (banco de dados, frameworks...)
