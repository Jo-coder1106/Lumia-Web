# LumIA Web

Sistema web acadêmico demonstrativo para gerenciamento de atividades e acompanhamento de entregas entre professores e alunos.

## Tecnologias
- Python 3.10 ou superior
- Flask
- SQLite
- HTML5 e CSS3

## Instalação e execução
1. Abra a pasta do projeto no terminal.
2. (Opcional) Crie um ambiente virtual: `python -m venv .venv`.
3. Ative o ambiente virtual:
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
   - Linux/macOS: `source .venv/bin/activate`
4. Instale as dependências: `pip install -r requirements.txt`.
5. Execute: `python app.py`.
6. Acesse `http://127.0.0.1:5000`.

O banco SQLite (`lumia.db`) é criado automaticamente na primeira execução.

## Contas demonstrativas
- Professor: `professor@lumia.com` / `123456`
- Aluno: `aluno@lumia.com` / `123456`

As contas são criadas apenas quando o banco de dados ainda não contém usuários.

## Funcionalidades
- Login com perfis de professor e aluno.
- Painel específico para cada perfil.
- Publicação de atividades pelo professor.
- Envio e atualização de respostas textuais pelo aluno.
- Consulta das entregas pelo professor.
- Registro de nota de 0 a 10 e feedback.

## Estrutura
- `app.py`: rotas, autenticação, regras de negócio e inicialização do banco.
- `templates/`: páginas HTML.
- `static/style.css`: estilos da interface.
- `requirements.txt`: dependências Python.
- `docs/`: documentação acadêmica.

## Equipe
- José Diego dos Santos Pinheiro
- Brenda Neves Reis
- Renan Matos Lima Magalhães
- Flávia Alessandra Moraes Resende
- Mariana Pollard Silva

## Segurança e limitações
Este repositório contém um protótipo acadêmico para execução e demonstração local, não uma aplicação pronta para produção. Para implantação pública, configure uma chave secreta forte pela variável de ambiente `LUMIA_SECRET_KEY`, desative o modo de depuração, use HTTPS e implemente proteção CSRF, política de senhas, recuperação de conta e limitação de tentativas. O sistema não possui envio de anexos, chat ou notificações. As entregas são feitas por texto.
