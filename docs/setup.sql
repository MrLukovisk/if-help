CREATE TABLE Usuario (
	ID INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(80) NOT NULL,
    email VARCHAR(80) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    tipo CHAR(1) NOT NULL DEFAULT 'N', /* Exite os tipos A = admin, P = professor. É necessário mudar o tipo da conta manualmente, não foi feito um menu de administração */
    pontos INT NOT NULL DEFAULT 0,
    PRIMARY KEY (ID)
);


CREATE TABLE Pergunta (
	ID INT NOT NULL AUTO_INCREMENT,
    titulo VARCHAR(255) NOT NULL,
    conteudo TEXT,
    usuario_id int,
    PRIMARY KEY (ID),
    FOREIGN KEY (usuario_id) REFERENCES Usuario(ID)
);


CREATE TABLE Resposta (
	ID INT NOT NULL AUTO_INCREMENT,
    conteudo TEXT,
    qtd_votos INT DEFAULT 0,
    usuario_id INT,
    pergunta_id INT,
    PRIMARY KEY (ID),
    FOREIGN KEY (usuario_id) REFERENCES Usuario(ID),
    FOREIGN KEY (pergunta_id) REFERENCES Pergunta(ID)
);


CREATE TABLE Voto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_voto ENUM('P', 'N') NOT NULL,
    usuario_id INT NOT NULL,
    resposta_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id),
    FOREIGN KEY (resposta_id) REFERENCES Resposta(id)
);