from flask import render_template, redirect, url_for, request, flash
from comunidade import app, database, bcrypt
#presisamos importa o form e instanciar dentro da função login
from comunidade.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
#criar usuario
from comunidade.models import Usuario, Post
#login
from flask_login import login_user, logout_user, current_user, login_required
#aula 38 -> o os servira para separar o nome da imagem
import secrets
import os
from PIL import Image

#aula 29 bloquear usuario q nao esteja logado, import login_required q é uma função usada como decorated, em todas as páginas q eu quero bloquear eu o uso
#caso ele nao esteja logado ele sera redirecionado p a pagina login, vai p init



# toda vez q for criar uma pagina deve começar assim: o ("\") é o caminho do site
#app.route é uma classe do flask
#decoration é uma função q vem antes de outra função, atribui uma nova funcionalidade a funcao def, faz com q ele apareça dentro do link
@app.route('/')
def home():
    #aula 44
    posts = Post.query.order_by(Post.id.desc())
    return render_template("home.html", posts=posts)
#retorne o arquivo html home, import antes o render_template


@app.route('/contato')
def contato():
    return render_template("contato.html")
       # "<p>fazendo errado</p>"
# render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    # aula 42 como  pegar  a   lista    de    usuario    do    banco    de    dados? Usuario.query.all
    lista_usuarios = Usuario.query.all()
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
            #aula 30 queremos redirecionar o usuario p a pagina q ele desejava antes de fazer login
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
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

#aula 28
#criar 3 link: 3 paginas: criar post, sair, meu perfil; se o cara ta logado aparece no menu
#importar o cara q identificar qm é o usuario q esta usando a ferramenta: current_user e vai p o navbar.html
@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso.', 'alert-success')
    return redirect(url_for('home'))
#import logout_user

@app.route('/perfil')
@login_required
def perfil():
    #foto_perfil recebe a foto do usario q sera carregada
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

#/post/criar pensando mais a frente pq eu posso apenas ver o post ou criar
@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    #import FormCriarPost e Post aula 43
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        # add post no banco de dados
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso', 'alert-success')
        return redirect(url_for('home'))
    # agora falta fazer o formulario do post no html
    return render_template('criarpost.html', form=form)


#aula 38
def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (200, 200)
    #instalar um cara p reduzir a imagem: pillow
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

#o q essa função tem q fazer p funcionar? percorrer os campos dos cursos e verificar qm esta marcado
def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)


#editar perfil aula 35
#aula 36 validar o button submit
@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        #preenche novo email
        current_user.email = form.email.data
        #preenche novo nome
        current_user.username = form.username.data
        #aula 38 edição e compactação da imagem de perfil
        if form.foto_perfil.data:
        #add um codigo aleatorio no nome da imagem -> reduzir o tamanho da imagem -> salvar a imagem na pasta -> mudar o campo foto-perfil do usuario p o novo nome da imagem
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        #aula 40 add os cursos -> criar uma função atualizar_cursos
        current_user.cursos = atualizar_cursos(form)
        #atualiza no banco de dados
        database.session.commit()
        flash('Perfil atualizado com sucesso.', 'alert-success')
        return redirect(url_for('perfil'))
    # aula 36 se o formulario for get? qdo o usuario for editar o formulario ja esta preenchido
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)