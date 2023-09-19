# Grudes API

Projeto de avaliação da primeira sprint do curso de Pós-graduação da PUC-Rio em Engenharia de Software.

Esta API fornece serviços para gerenciar receitas culinárias, armazenando-as em um banco de dados.
Dentre os serviços, podemos destacar o cadastro de ingredientes e receitas e a busca de receitas por
ingredientes. 

---
## Requisitos 
* Sistema Operacional Unix.
* Docker Compose >= 2.5.0 instalado.
* Permissão de execução do docker como superusuário.

---
## Execução
Na raiz deste repositório, executar:
```sh
$ sudo docker compose up --build 
```
Ou para modo desenvolvimento:
```sh
$ sudo docker compose -f docker-compose.yml -f dev.yml up --build 
```

Abra http://localhost:5001/#/ no navegador para ver a documentação da API em execução.
