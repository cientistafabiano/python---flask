#para o models funcionar ele precisa do database
#qdo estiver dentro do init nao precisa colocar ele
from comunidade import database, login_manager
from datetime import datetime
from flask_login import UserMixin

#login_manager precisa de uma função para encontrar o usuario pelo id dele
#user_loader carrega essa função
#criar uma função para encontrar o usuario de acordo com o id dele
#o get encontra um item da tabela de acordo com a primary_key
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))
#qual é a tabela q tem a estrutura de usuario q ele precisa, import UserMixin q é um parametro q vamos passa p a classe p atribuir caracteristicas q o login_manager precisa

#as classes sao as estruturas da tabela do banco de dados
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)
# cada usuario pode ter muitos posts, relação um p muitos: posts = database.relationship()
#como fazer para relacionar: com o backref=autor
    cursos = database.Column(database.String, nullable=False, default='Não informado')

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
 #a chave estrangeira(foreignKey) q relaciona as tabelas



#para criar o banco de dados temos q ir no python console e importa do main o database, e do models o Usuario e o Post
#depois criar com: database.create_all()
#depois criar o usuario (o minimo de informação necessarias sao o username, email, senha)
# usuario = Usuario(username="Fabiano", email="azedias@gmail.com", senha="1234")
#criou-se uma variavel q é uma instancia do usuario
#precisa registrar esse usuario dentro do banco de dados, como:
#database.session.add(usuario)
#database.session.commit()
#saber qm foi add ao bd: Usuario.query.all()
#consultar qm sao os usuarios: Usuario.query.first()
#cria uma variavel p poder consultar: usuario_test = Usuario.query.first()
# usuario_test.email; usuario_test.username
#pegar um usuario em especifico: usuario_test2 = Usuario.query.filter_by(email='azedias@gmail.com')
#query é uma lista
#como fazer p criar posts?
# criar uma instancia (post1 = Post(titulo='Post do Fabiano', corpo='seguimos estudando python', id_usuario=1))
#add na pasta temporaria (database.session.add(post1)) e depois dar commit(database.session.commit())
#visualizar: Post.query.all(), depois: post1 = Post.query.first(), post1.corpo, post1.autor
#saber o usuario do post: autor_post1 = post1.autor; autor_post1.posts; autor_post1.username
#deletar o banco de dados: database.drop_all()
