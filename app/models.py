from flask_sqlalchemy import SQLAlchemy

# conectando o slqalchemy
db = SQLAlchemy()

# banco de dados (tabelas)
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(1), default='N')
    pontos = db.Column(db.Integer, default=0)
    perguntas = db.relationship('Pergunta', backref='usuario')
    respostas = db.relationship('Resposta', backref='usuario')
    votos = db.relationship('Voto', backref='usuario')

    @staticmethod
    def atualizar_pontos(usuario_id):
        from sqlalchemy.sql import func 
        
        total_pontos = db.session.query(func.sum(Resposta.qtd_votos))\
            .filter_by(usuario_id=usuario_id).scalar() or 0
            
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            usuario.pontos = total_pontos
            db.session.commit()

class Pergunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    respostas = db.relationship('Resposta', backref='pergunta')

class Resposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    qtd_votos = db.Column(db.Integer, default=0)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    pergunta_id = db.Column(db.Integer, db.ForeignKey('pergunta.id'), nullable=False)
    votos = db.relationship('Voto', backref='resposta')

class Voto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_voto = db.Column(db.String(1), nullable=False)  # 'P' para positivo, 'N' para negativo
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    resposta_id = db.Column(db.Integer, db.ForeignKey('resposta.id'), nullable=False)
