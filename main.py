#como vem do arquivo init
from comunidade import app

# inicia o site
# debug=true atualiza a pagina
if __name__ == '__main__':
    app.run(debug=True)


# os arquivos html tem q estar detro da pasta templates

#função do flask q altera o link em todos os lugares , nunca mudar o nome da função pq o link pode ser alterado
# sempre usar funçao url_for para link: pegue o link da função x, alterar no navbar.html