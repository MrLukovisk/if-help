from flask import render_template, request, session, flash, redirect, url_for, current_app as app
from sqlalchemy.sql import func
from .models import db, Usuario, Pergunta, Resposta, Voto
from werkzeug.security import check_password_hash, generate_password_hash

# rotas
@app.route('/', methods=("GET", "POST"))
def home():

    # ordena as perguntas de modo crescente por respostas (se ninguem respondeu, aparece em cima)
    if request.method == "POST":
        pesquisa = request.form["pesquisa"]
    
        posts = Pergunta.query \
            .outerjoin(Resposta) \
            .filter(
                Pergunta.titulo.ilike(f'%{pesquisa}%') |  # pesquisa no titulo e conteudo
                Pergunta.conteudo.ilike(f'%{pesquisa}%')  
            ) \
            .group_by(Pergunta.id) \
            .order_by(func.count(Resposta.id).desc()) \
            .all()
    else:
        posts = Pergunta.query \
            .outerjoin(Resposta) \
            .group_by(Pergunta.id) \
            .order_by(func.count(Resposta.id).asc()) \
            .all()
        

    # poder mudar de pagina la em baixo
    pagina = request.args.get('pagina', default=1, type=int)
    qtd_posts_pag = 10
    inicio = (pagina - 1) * qtd_posts_pag
    fim = inicio + qtd_posts_pag
    posts_mostrar = posts[inicio:fim]
    total_paginas = (len(posts) + qtd_posts_pag - 1) // qtd_posts_pag
    if total_paginas == 0:
        total_paginas = 1

    if "email" in session:
        return render_template("home.html", posts=posts_mostrar, pagina=pagina, total_paginas=total_paginas, logado=True)
    else:
        return render_template("home.html", posts=posts_mostrar, pagina=pagina, total_paginas=total_paginas, logado=False)

@app.route("/login", methods=("GET", "POST"))
def login():
    if "email" in session:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        if not email or not senha:
            flash("Por favor, preencha todos os campos.")
            return redirect(url_for("login"))
        else:
            usuario_login = Usuario.query.filter_by(email=email).first()

            if usuario_login:
                if check_password_hash(usuario_login.senha, senha):
                    session["email"] = email
                    session["tipo"] = usuario_login.tipo
                    session["id"] = usuario_login.id
                    return redirect(url_for("home"))
                else:
                    flash("Algo está errado, tente novamente.")
            else: 
                flash("Usuário não encontrado. Tente novamente.")

    return render_template("login.html")

@app.route("/registrar", methods=("GET", "POST"))
def registrar():
    if "email" in session:
        return redirect(url_for("home"))

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        usuario_existente = Usuario.query.filter_by(email=email).first()

        if not nome:
            flash("Coloque o seu nome.")
        elif not email:
            flash("Coloque o seu email.")
        elif not senha:
            flash("Coloque a sua senha.")
        elif usuario_existente:
            flash("Este usuario já existe.")
        else:
            senha_hash = generate_password_hash(senha)
            usuario = Usuario(nome=nome,
                            email=email,
                            senha=senha_hash)
            db.session.add(usuario)
            db.session.commit()
            session["email"] = email
            session["tipo"] = "N"
            session["id"] = usuario.id

            return redirect(url_for('home'))

    return render_template("registrar.html")

@app.route("/postar", methods=("GET", "POST"))
def postar():

    if "email" not in session:
        return redirect(url_for("login"))

    usuario = Usuario.query.filter_by(email=session["email"]).first()
    if request.method == 'POST':
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']

        if not titulo:
            flash("Coloque um titulo.")
        else:
            pergunta = Pergunta(titulo=titulo,
                            conteudo=conteudo,
                            usuario_id=usuario.id)
            db.session.add(pergunta)
            db.session.commit()

            return redirect(url_for('home'))
    
    return render_template("postar.html", logado=True)

@app.route("/logout")
def logout():
    if "email" in session:
        session.pop("email", None)
        session.pop("tipo", None)
    return redirect(url_for("home"))

@app.route("/user/<int:user_id>", methods=("GET", "POST"))
def show_user(user_id):
    user = Usuario.query.get_or_404(user_id)

    posts = Pergunta.query \
        .filter_by(usuario_id = user.id) \
        .order_by(Pergunta.id.desc()) \
        .all()
    
    pagina = request.args.get('pagina', default=1, type=int)
    qtd_posts_pag = 10
    inicio = (pagina - 1) * qtd_posts_pag
    fim = inicio + qtd_posts_pag
    posts_mostrar = posts[inicio:fim]
    total_paginas = (len(posts) + qtd_posts_pag - 1) // qtd_posts_pag
    if total_paginas == 0:
        total_paginas = 1
        
    if "email" in session:
        return render_template("usuario.html", usuario=user, posts=posts_mostrar, pagina=pagina, total_paginas=total_paginas, logado=True)
    else:
        return render_template("usuario.html", usuario=user, posts=posts_mostrar, pagina=pagina, total_paginas=total_paginas)

@app.route('/post/<int:post_id>', methods=("GET", "POST"))
def show_post(post_id):
    post = Pergunta.query.get_or_404(post_id)
    
    respostas = Resposta.query \
        .filter_by(pergunta_id=post.id) \
        .order_by(Resposta.qtd_votos.desc()) \
        .all()

    # poder mudar de pagina la em baixo
    pagina = request.args.get('pagina', default=1, type=int)
    qtd_posts_pag = 10
    inicio = (pagina - 1) * qtd_posts_pag
    fim = inicio + qtd_posts_pag
    respostas_mostrar = respostas[inicio:fim]
    total_paginas = (len(respostas) + qtd_posts_pag - 1) // qtd_posts_pag
    if total_paginas == 0:
        total_paginas = 1

    if "email" in session:
        user = Usuario.query.filter_by(email = session["email"]).first()

        if request.method == "POST":
            conteudo = request.form["conteudo"]
            if not conteudo:
                flash("Escreva algo antes de responder.")
            else:
                resposta = Resposta(conteudo=conteudo,
                                    qtd_votos=0,
                                    usuario_id=user.id,
                                    pergunta_id=post.id)
                db.session.add(resposta)
                db.session.commit()
                return redirect(url_for("show_post", post_id=post.id))
            
        return render_template("post.html", post=post, usuario=user, respostas=respostas_mostrar, total_paginas=total_paginas, pagina=pagina, logado=True)
    else:
        return render_template("post.html", post=post, respostas=respostas_mostrar, total_paginas=total_paginas, pagina=pagina, logado=False)

@app.route('/votar/<int:resposta_id>/<tipo_voto>', methods=["GET"])
def votar(resposta_id, tipo_voto):

    resposta = Resposta.query.get_or_404(resposta_id)

    if "email" not in session:
        return redirect(url_for("show_post", post_id=resposta.pergunta_id))
    
    usuario = Usuario.query.filter_by(email=session["email"]).first()
    
    # Verificar se o usuário já votou na resposta
    voto_existente = Voto.query.filter_by(usuario_id=usuario.id, resposta_id=resposta.id).first()
    
    if voto_existente:
        # Se o usuário já votou e tenta votar igual, deleta
        if voto_existente.tipo_voto == tipo_voto:
            db.session.delete(voto_existente)
        else:
            voto_existente.tipo_voto = tipo_voto  # Atualiza o tipo de voto (positivo ou negativo)
            db.session.commit()
    else:
        # Caso o usuário não tenha votado, cria um novo voto
        novo_voto = Voto(tipo_voto=tipo_voto, usuario_id=usuario.id, resposta_id=resposta.id)
        db.session.add(novo_voto)
        db.session.commit()
    
    # Atualiza os votos da resposta (conta todos votos positivos e negativos)
    votos_positivos = Voto.query.filter_by(resposta_id=resposta.id, tipo_voto='P').count()
    votos_negativos = Voto.query.filter_by(resposta_id=resposta.id, tipo_voto='N').count()
    resposta.qtd_votos = votos_positivos - votos_negativos
    db.session.commit()

    Usuario.atualizar_pontos(resposta.usuario_id)
 
    return redirect(url_for("show_post", post_id=resposta.pergunta_id))

@app.route('/deletar_postagem/<int:post_id>', methods=("GET", "POST"))
def deletar_postagem(post_id):
    if "email" not in session:
        return redirect(url_for("show_post", post_id=post_id))

    user = Usuario.query.filter_by(email=session["email"]).first()
    post = Pergunta.query.get_or_404(post_id)

    if user.tipo == "A" or post.usuario_id == user.id:
        # Exclui todas as respostas associadas à postagem
        respostas = Resposta.query.filter_by(pergunta_id=post_id).all()
        for resposta in respostas:
            deletar_resposta(resposta.id)

        # Exclui a postagem
        db.session.delete(post)
        db.session.commit()

        flash("Postagem e suas respostas foram excluídas com sucesso.")
        return redirect(url_for('home'))
    else:
        return redirect(url_for('show_post', post_id=post_id))
    

@app.route('/deletar_resposta/<int:resposta_id>')
def deletar_resposta(resposta_id):
    if "email" not in session:
        return redirect(url_for("show_post", post_id=resposta_id))

    user = Usuario.query.filter_by(email=session["email"]).first()
    resposta = Resposta.query.get_or_404(resposta_id)

    if user.tipo == "A" or resposta.usuario_id == user.id:
        Voto.query.filter_by(resposta_id=resposta_id).delete()
        db.session.delete(resposta)
        db.session.commit()

        return redirect(url_for("show_post", post_id=resposta.pergunta_id))
    else:
        flash("Ação não permitida.")
        return redirect(url_for('show_post', post_id=resposta_id))