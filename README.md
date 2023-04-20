# Grudes API

Projeto de avaliação da primeira sprint do curso de Pós-graduação da PUC-Rio em Engenharia de Software.

Esta API fornece serviços para gerenciar receitas culinárias, armazenando-as em um banco de dados.
Dentre os serviços, podemos destacar o cadastro de ingredientes e receitas e a busca de receitas por
ingredientes. 

---
## Como executar 

```
$ cd grudes_api
$ python3 -m venv env
$ source env/bin/activate
(env)$ pip install -r requirements.txt
(env)$ flask run --host 0.0.0.0 --port 5001

# Ou para mode desenvolvimento
(env)$ flask run --host 0.0.0.0 --port 5001 --reload

```

Abra o [http://localhost:5001/#/](http://localhost:5001/#/) no navegador para ver a documentação da API em execução.
