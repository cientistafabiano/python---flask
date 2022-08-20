from flask import render_template, redirect, url_for, request, flash
from comunidade import app, database, bcrypt
#presisamos importa o form e instanciar dentro da função login
from comunidade.forms import FormLogin, FormCriarConta
#criar usuario
from comunidade.models import Usuario
#login
from flask_login import login_user



#para ter usuarios temos q ter uma lista
lista_usuarios = ['Fabiano', 'Joelson', 'Marisa', 'Rafa', 'Raul']


# toda vez q for criar uma pagina deve começar assim, o ("\") é o caminho do site
#app.route é uma classe do flask
#decoration é uma função q vem antes de outra função, atribui uma nova funcionalidade a funcao def, faz com q ele apareça dentro do link
@app.route('/ola')
def hello_world():
    return "<p>sexta-feira 12 de agosto 2022 16:20</p><p>quarta-feira 17 de agosto 2022 19:02</p>"


@app.route('/')
def home():
    return render_template("home.html")
#   "<p>fazendo errado</p>"
#retorne o arquivo html home, import antes o render_templates


@app.route('/contato')
def contato():
    return render_template("contato.html")
       # "<p>fazendo errado</p>"
# render_template('contato.html')

@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

#como importa p dentro do site? igual foi feito em lista_usuarios
#os objetos criados nesta função sao usados em login.html
#na funcao deve permitir o method post em todas as paginas q tem form
@app.route('/login', methods=['GET', 'POST'])
def login_criar_conta():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    # essa segunda condição só tem pq estao na mesma pagina
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            #como fazer o login?
            #remember é para checkbox lembrar dados
            login_user(usuario, remember=form_login.lembrar_dados.data)
            #fez o login com sucesso tela verde
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            # redirecionar para a pagina home
            return redirect(url_for('home'))
        else:
            flash(f'Falha no login. E-mail ou senha incorretos', 'alert-danger')
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        #criar o usuario; add a session; dar commit; criptografia da senha
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        #importa o banco de dados
        database.session.add(usuario)
        database.session.commit()
        #criou conta com sucesso
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login_criarConta.html', form_login=form_login, form_criarconta=form_criarconta)