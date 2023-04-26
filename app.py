from flask import Flask, render_template, request, redirect, url_for
from mongoengine import connect, Document, StringField, BooleanField, DateTimeField, ReferenceField, ListField

connect(host='mongodb+srv://fkenjiyunoki:python123@cluster0.r7wsj9k.mongodb.net/test')

app = Flask(__name__)

class Usuario(Document):
    nome = StringField(required=True, max_length=50)
    email = StringField(required=True, max_length=50)
    senha = StringField(required=True)

class Projeto(Document):
    titulo = StringField(required=True, max_length=50)
    descricao = StringField(required=True)
    criador = ReferenceField(Usuario)
    tarefas = ListField(ReferenceField('Tarefa'))

class Tarefa(Document):
    titulo = StringField(required=True, max_length=50)
    descricao = StringField(required=True)
    prazo = DateTimeField(required=True)
    concluida = BooleanField(required=True)
    projeto = ReferenceField(Projeto)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.objects(email=email, senha=senha).first()
        if usuario:
            return redirect(url_for('projetos'))
    return render_template('login.html')

@app.route('/usuarios')
def usuarios():
    usuarios = Usuario.objects()
    return render_template('listarUsuario.html', usuarios=usuarios)

@app.route('/projetos')
def projetos():
    projetos = Projeto.objects()
    return render_template('cadastroProjetos.html', projetos=projetos)

@app.route('/projetos/cadastrar', methods=['GET', 'POST'])
def cadastrar_projeto():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        projeto = Projeto(titulo=titulo, descricao=descricao)
        projeto.save()
        return redirect(url_for('projetos'))
    return render_template('cadastroProjetos.html')

@app.route('/projetos/<id>/editar', methods=['GET', 'POST'])
def editar_projeto(id):
    projeto = Projeto.objects(id=id).first()
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        projeto.titulo = titulo
        projeto.descricao = descricao
        projeto.save()
        return redirect(url_for('projetos'))
    return render_template('listarProjetos.html', projeto=projeto)

@app.route('/projetos/<id>/excluir', methods=['POST'])
def excluir_projeto(id):
    projeto = Projeto.objects(id=id).first()
    projeto.delete()
    return redirect(url_for('projetos'))

@app.route('/projetos/<id>/tarefas')
def tarefas(id):
    projeto = Projeto.objects(id=id).first()
    tarefas = Tarefa.objects(projeto=projeto)
    return render_template('listarTarefas.html', projeto=projeto, tarefas=tarefas)

@app.route('/projetos/<id>/tarefas/cadastrar', methods=['GET', 'POST'])
def cadastrar_tarefa(id):
    projeto = Projeto.objects(id=id).first()
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        prazo = request.form['prazo']
        tarefa = Tarefa(titulo=titulo, descricao=descricao, prazo=prazo, concluida=False, projeto=projeto)
        tarefa.save()
        return redirect(url_for('tarefas', id=id))
    return render_template('cadastroTarefas.html', projeto=projeto)

@app.route('/projetos/<id_projeto>/tarefas/<id_tarefa>/editar', methods=['GET', 'POST'])
def editar_tarefa(id_projeto, id_tarefa):
    projeto = Projeto.objects(id=id_projeto).first()
    tarefa = Tarefa.objects(id=id_tarefa).first()
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        prazo = request.form['prazo']
        concluida = True if request.form.get('concluida') else False
        tarefa.titulo = titulo
        tarefa.descricao = descricao
        tarefa.prazo = prazo
        tarefa.concluida = concluida
        tarefa.save()
        return redirect(url_for('tarefas', id=id_projeto))
    return render_template('listarTarefas.html', projeto=projeto, tarefa=tarefa)

@app.route('/projetos/<id_projeto>/tarefas/<id_tarefa>/excluir', methods=['POST'])
def excluir_tarefa(id_projeto, id_tarefa):
    tarefa = Tarefa.objects(id=id_tarefa).first()
    tarefa.delete()
    return redirect(url_for('tarefas', id=id_projeto))