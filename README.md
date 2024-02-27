# ADA API

## REQUISITOS
- Linux
- Python 3.11.6
- PostgreSQL
- Redis

## COMO USAR
Faça o clone do projeto:

```git clone git@github.com:fernandogfleite/ada-api.git```

Entre na pasta do projeto, crie uma virtualenv e ative-a:

```python -m venv venv```

```source venv/bin/activate```

Instale as dependências do projeto:

```pip install -r requirements.txt```


Crie um arqivo e o nomeie como .env e o preencha de acordo com o arquivo .env-example

Estando com o .env preenchido rode o seguinte comando para aplicar as migrations no seu banco de dados:

```python manage.py migrate```

Feito isso crie seu superusuário:

```python manage.py createsuperuser```

Agora rode a aplicação:

```python manage.py runserver```

Rota administrativa:
[http://localhost:8000/admin/](http://localhost:8000/admin/)