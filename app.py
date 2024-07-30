import requests as requests
from flask import Flask, render_template, request, redirect, url_for, flash
import urllib.request, json
from flask_sqlalchemy import SQLAlchemy
import git

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskbd.sqlite3'

urllist = ['https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&language=pt-BR&api_key=3cb2c7a46041563eca34558a6ff11b9d', 'https://api.themoviedb.org/3/discover/movie?language=pt-BR&certification.lte=A&sort_by=popularity.desc&certification_country=BG&page=1&api_key=3cb2c7a46041563eca34558a6ff11b9d', 'https://api.themoviedb.org/3/trending/tv/week?language=pt-BR&api_key=3cb2c7a46041563eca34558a6ff11b9d', 'https://api.themoviedb.org/3/discover/movie?include_adult=true&include_video=false&language=pt-BR&page=1&sort_by=popularity.desc&with_genres=27&api_key=3cb2c7a46041563eca34558a6ff11b9d', 'https://api.themoviedb.org/3/movie/upcoming?language=pt-BR&page=1&api_key=3cb2c7a46041563eca34558a6ff11b9d']
db = SQLAlchemy(app)
book = []
registros = []

class bd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(150))
    avg = db.Column(db.Integer)

    def __init__(self, nome, descricao, avg):
        self.nome = nome
        self.descricao = descricao
        self.avg = avg

def get_dados():
    global jsondata
    global jsondatakids
    global jsondataseries
    global jsondataterror
    global jsondatabreve

    resposta_filme = urllib.request.urlopen(urllist[0])
    dados_filme = resposta_filme.read()
    jsondata = json.loads(dados_filme)

    resposta_filmekids = urllib.request.urlopen(urllist[1])
    dados_filmekids = resposta_filmekids.read()
    jsondatakids = json.loads(dados_filmekids)

    resposta_series = urllib.request.urlopen(urllist[2])
    dados_series = resposta_series.read()
    jsondataseries = json.loads(dados_series)

    resposta_filmeterror = urllib.request.urlopen(urllist[3])
    dados_filmeterror = resposta_filmeterror.read()
    jsondataterror = json.loads(dados_filmeterror)

    resposta_filmebreve = urllib.request.urlopen(urllist[4])
    dados_filmebreve = resposta_filmebreve.read()
    jsondatabreve = json.loads(dados_filmebreve)

@app.route('/', methods=["GET", "POST"])
def main():
    try:
        livro = ("Rita Lobo")
        registros.append({"livro": request.form.get("livro")})
        url = f'https://www.googleapis.com/books/v1/volumes?q={livro}'
        get_dados()
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return render_template("index.html", registros=registros, topresults='', filmes=jsondata['results'], filmeskids=jsondatakids['results'], series=jsondataseries['results'], filmesterror=jsondataterror['results'], filmesbreve=jsondatabreve['results'])
    try:
        topresults = response.json()
        return render_template("index.html", registros=registros, topresults=topresults['items'], filmes=jsondata['results'], filmeskids=jsondatakids['results'], series=jsondataseries['results'], filmesterror=jsondataterror['results'], filmesbreve=jsondatabreve['results'])
    except (KeyError, TypeError, ValueError):
        return render_template("index.html", registros=registros, topresults='', filmes=jsondata['results'], filmeskids=jsondatakids['results'], series=jsondataseries['results'], filmesterror=jsondataterror['results'], filmesbreve=jsondatabreve['results'])

@app.route('/sobre/<propriedade>', methods=["GET", "POST"])
def sobre(propriedade):
    if propriedade == 'search':
        if request.method == "POST":
            try:
                if request.form.get("livro"):
                    livro = request.form.get("livro")
                    registros.append({"livro": request.form.get("livro")})
                    url = f'https://www.googleapis.com/books/v1/volumes?q={livro}'
                    response = requests.get(url)
                    response.raise_for_status()
            except requests.RequestException:
                return render_template("sobre.html", registros=registros, topresults='')
            try:
                topresults = response.json()
                return render_template("sobre.html", registros=registros, topresults=topresults['items'])
            except (KeyError, TypeError, ValueError):
                return render_template("sobre.html", registros=registros, topresults='')
        else:
            return render_template("sobre.html", registros=registros, topresults='')

@app.route('/filme/<propriedade>', methods=["GET", "POST"])
def filme(propriedade):
    if propriedade == 'populares':
        url = 'https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&language=pt-BR&api_key=3cb2c7a46041563eca34558a6ff11b9d'
    elif propriedade == 'kids':
        url = 'https://api.themoviedb.org/3/discover/movie?language=pt-BR&certification.lte=A&sort_by=popularity.desc&certification_country=BG&page=1&api_key=3cb2c7a46041563eca34558a6ff11b9d'
    elif propriedade == 'series':
        url = 'https://api.themoviedb.org/3/trending/tv/week?language=pt-BR&api_key=3cb2c7a46041563eca34558a6ff11b9d'
    elif propriedade == 'terror':
        url = 'https://api.themoviedb.org/3/discover/movie?include_adult=true&include_video=false&language=pt-BR&page=1&sort_by=popularity.desc&with_genres=27&api_key=3cb2c7a46041563eca34558a6ff11b9d'
    elif propriedade == 'breve':
        url = 'https://api.themoviedb.org/3/movie/upcoming?language=pt-BR&page=1&api_key=3cb2c7a46041563eca34558a6ff11b9d'
    elif propriedade == 'books':
        url = 'https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?api-key=01qBFr8mJz1osGUv7ywyppwGq6gIOD6E'
    resposta = urllib.request.urlopen(url)
    dados = resposta.read()
    jsondata = json.loads(dados)
    if request.method == 'POST':
        if request.form.get("filme") and request.form.get("nota"):
            registros.append({"filme": request.form.get("filme"), "nota": request.form.get("nota")})
    return render_template("filme.html", filmes=jsondata['results'])

@app.route('/favlivros')
def lista_livros():
    page = request.args.get('page', 1, type=int)
    per_page = 4
    all_livros = bd.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("favlivros.html", bd=all_livros)

@app.route('/addlivros', methods=["GET", "POST"])
def add_livros():
    nome = request.form.get("nome")
    descricao = request.form.get("descricao")
    avg = request.form.get("avg")
    if request.method == 'POST':
        if not nome or not descricao or not avg:
            flash("Preencha todos os campos", "error")
        else:
            bd_post = bd(nome,descricao,avg)
            db.session.add(bd_post)
            db.session.commit()
            return redirect(url_for('lista_livros'))
    return render_template("addlivros.html")

@app.route('/<int:id>/atualiza_livro', methods=["GET", "POST"])
def atualiza_livro(id):
    livro = bd.query.filter_by(id=id).first()
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        avg = request.form['avg']
        bd.query.filter_by(id=id).update({"nome": nome, "descricao": descricao, "avg": avg})
        db.session.commit()
        return redirect(url_for('lista_livros'))
    return render_template("atualiza_livro.html", livro=livro)

@app.route('/<int:id>/remove_livro')
def remove_livro(id):
    livro = bd.query.filter_by(id=id).first()
    db.session.delete(livro)
    db.session.commit()
    return redirect(url_for('lista_livros'))

if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    #serve(app, port='8000')
    app.config['SECRET_KEY'] = 'app'
    app.run(host='0.0.0.0', debug=True)