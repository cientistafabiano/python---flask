#sempre q chamar a pasta comunidade roda o __init__
# aqui importamos o framework flask
from flask import Flask

#banco de dados
from flask_sqlalchemy import SQLAlchemy
#para criar usuario e post
#qdo faço essa importação da um erro pq no models estamos importando o main, para isso teremos q colocar os arquivos todos dentro da mesma pasta
#o arquivo main servira apenas p iniciar o app

#criptografia de senha
from flask_bcrypt import Bcrypt

#para login
from flask_login import LoginManager

# aqui cria o site q no pycharm chama app
app = Flask(__name__)

#passo a passo pa ter uma nova pagina no site: criar uma função com route; criar arquivo html; direcionar os links


#segurança para as senhas
#todo site tem q ter o csrf_token e ele vai logo a baixo do form
app.config['SECRET_KEY'] = '7ef8f1a96cdfe6440bfabe157d4027c1'
#PARA CRIAR A SENHA FAZ USO DO TERMINAL: python enter; import secrets enter; secrets.token_hex(16) enter;

#banco de dados
#configurar o app q ficara o banco de dados, uri é link interno, sqlite cria o banco de dados e salva e main.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
database = SQLAlchemy(app)
#quais sao as informações q eu quero guardar? os usuarios e todas as informações dele, posts e as informações de horario, title ...
#SQLAlchemy possibilita criar o banco de dados em formato de classe

#instancia da classe Bcrypt
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

#chama no fim para poder chamar os links depois q chama o app
from comunidade import routes