Projeto Final Interdisciplinar - Lucas Brand

Esse projeto foi realizado com o intuito de facilitar a comunicação organizacional utilizando um site de perguntas e respostas, tendo como foco a ajuda escolar daqueles na instituição.

===

Tecnologias utilizadas:
* Python 
* Flask
* SQLAlchemy
* MySQL
* PyMySQL

---

Estrutura do projeto:

projeto/
|
|-- app/
|   |-- static/          # CSS e Imagens
|   |-- templates/       # HTMLs
|   |-- __init__.py      # Setup
|   |-- models.py        # Classes do Banco de Dados
|   |-- routes.py        # Rotas 
|   
|
|-- docs/
|   |-- README.md       
|   |-- requirements.txt # Requerimentos
|   |-- setup.sql        # O código sql para criar as tabelas
|
|-- .env                 # Variáveis sensíveis
|-- main.py              # Inicialização


---

Como Configurar e Rodar:

1. Clonar o repositório
bash
git clone [https://github.com/MrLukovisk/if-help.git]

2. Configurar o Ambiente Virtual
python -m venv .venv
# Ativação (Windows):
.venv\Scripts\activate
# Ativação (Linux/Mac):
source .venv/bin/activate

3. Instalar Dependências
pip install -r docs/requirements.txt

4. Variáveis de Ambiente
Crie um arquivo .env dentro da pasta projeto/ e adicione suas strings sensíveis:
SECRET_KEY=CHAVE_SECRETA
DATABASE_URL=mysql+pymysql://USUARIO:SENHA@localhost/NOME_DO_BANCO

5. Execução e Banco de Dados
Para iniciar o servidor, execute:
python main.py

---

Referência Técnica (SQL)
Para fins de consulta ou migração manual, o script original de criação das tabelas (DDL) está disponível em:
docs/setup.sql
