# LumIA Web

Sistema web acadêmico demonstrativo para gerenciamento de atividades e acompanhamento de entregas entre professores e alunos.

## Executar no Windows sem instalar Python

1. Baixe o artefato **LumIA-Web-Windows-x64.zip** na aba **Actions** do GitHub.
2. Extraia o ZIP para uma pasta comum, por exemplo, Área de Trabalho\LumIA Web.
3. Abra `LumIA-Web.exe` com duplo clique.
4. O navegador será aberto automaticamente no endereço local exibido na janela.
5. Para encerrar o servidor, feche a janela preta ou pressione Ctrl+C nela.

O executável é destinado ao Windows 10/11 de 64 bits e inclui o Python e as dependências necessárias. Não requer instalação de Python.

**Importante:** mantenha o arquivo `lumia.db` ao lado do executável depois da primeira execução. Ele contém as atividades e respostas cadastradas. Faça cópias de segurança desse arquivo antes de atualizar o programa. Se a pasta estiver protegida pelo Windows, mova-a para Documentos ou Área de Trabalho.

## Contas demonstrativas
- Professor: `professor@lumia.com` / `123456`
- Aluno: `aluno@lumia.com` / `123456`

As contas são criadas apenas quando o banco de dados ainda não contém usuários.

## Executar a partir do código-fonte

Requer Python 3.10 ou superior:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Acesse http://127.0.0.1:5000.

## Funcionalidades
- Login com perfis de professor e aluno.
- Painel específico para cada perfil.
- Publicação de atividades pelo professor.
- Envio e atualização de respostas textuais pelo aluno.
- Consulta das entregas pelo professor.
- Registro de nota de 0 a 10 e feedback.

## Documentação acadêmica
A documentação do projeto está em [docs/Documentacao_LumIA_Web.md](docs/Documentacao_LumIA_Web.md).

## Equipe
- José Diego dos Santos Pinheiro (RA 5779944)
- Brenda Neves Reis (RA 5810531)
- Renan Matos Lima Magalhães (RA 5696313)
- Flávia Alessandra Moraes Resende (RA 5116520)
- Mariana Pollard Silva (RA 5727944)

## Segurança e limitações
Este repositório contém um protótipo acadêmico para execução e demonstração local, não uma aplicação pronta para produção. Para implantação pública, configure uma chave secreta forte pela variável de ambiente `LUMIA_SECRET_KEY`, desative o modo de depuração, use HTTPS e implemente proteção CSRF, política de senhas, recuperação de conta e limitação de tentativas. O servidor do executável escuta somente em `127.0.0.1`, não publica o sistema na rede. O sistema não possui envio de anexos, chat ou notificações.
