# Universidade Santo Amaro (UNISA)
## Projeto Integrador de Programação WEB
# LumIA Web
### Sistema WEB de gerenciamento e acompanhamento acadêmico

**Repositório:** https://github.com/Jo-coder1106/Lumia-Web  
**São Paulo, 2026**

## Identificação do projeto

**Título:** LumIA Web: Sistema WEB de gerenciamento e acompanhamento acadêmico.  
**Área temática:** Programação WEB.  
**Natureza:** Protótipo acadêmico funcional.  
**Tecnologias:** Python, Flask, HTML5, CSS3, JavaScript e SQLite.  
**Orientador(a):** preencher conforme orientação da disciplina.

### Integrantes

| Integrante | RA |
|---|---:|
| José Diego dos Santos Pinheiro | 5779944 |
| Brenda Neves Reis | 5810531 |
| Renan Matos Lima Magalhães | 5696313 |
| Flávia Alessandra Moraes Resende | 5116520 |
| Mariana Pollard Silva | 5727944 |

## Resumo

O LumIA Web é uma aplicação WEB proposta para apoiar o acompanhamento de atividades acadêmicas por meio da interação entre professores e alunos. O sistema permite que o professor publique atividades, consulte as respostas recebidas e registre notas e feedbacks. O aluno pode visualizar as atividades disponíveis, enviar ou atualizar suas respostas e consultar a avaliação recebida. A solução foi implementada como uma aplicação WEB utilizando Python com o microframework Flask no lado do servidor, páginas HTML, estilos CSS e banco de dados SQLite. O projeto prioriza um escopo reduzido, de fácil instalação e adequado à demonstração dos conceitos fundamentais de desenvolvimento WEB, persistência de dados, autenticação e controle de acesso por perfil.

**Palavras-chave:** Programação WEB; educação; atividades acadêmicas; Flask; SQLite.

## 1. Introdução

A utilização de sistemas WEB permite disponibilizar funcionalidades por meio de navegadores, reduzindo a necessidade de instalação de programas específicos nos dispositivos dos usuários. No contexto educacional, ferramentas digitais podem centralizar informações sobre atividades, entregas e devolutivas, facilitando o acompanhamento do processo de aprendizagem.

O LumIA Web foi concebido como uma aplicação simples para organizar parte desse fluxo. A proposta contempla dois perfis principais: professor e aluno. Cada perfil acessa funcionalidades adequadas à sua responsabilidade, mantendo as informações das atividades e entregas armazenadas em um banco de dados.

## 2. Problema e justificativa

A distribuição de atividades e o acompanhamento de respostas podem ficar dispersos entre diferentes canais de comunicação. Essa dispersão dificulta a consulta do histórico e a identificação do retorno dado aos alunos.

O projeto busca centralizar esse processo em uma aplicação WEB de pequeno porte. A escolha se justifica pela possibilidade de demonstrar, em um cenário concreto, a integração entre interface, lógica de servidor, banco de dados e controle de acesso.

## 3. Objetivos

### 3.1 Objetivo geral

Desenvolver uma aplicação WEB para gerenciamento de atividades acadêmicas, envio de respostas e registro de feedback entre professores e alunos.

### 3.2 Objetivos específicos

- Implementar autenticação de usuários.
- Separar as funcionalidades conforme o perfil de professor ou aluno.
- Permitir que professores publiquem atividades e definam datas de entrega.
- Permitir que alunos consultem atividades e enviem ou atualizem respostas.
- Permitir que professores consultem entregas, registrem notas de zero a dez e escrevam feedback.
- Persistir usuários, atividades e entregas em banco de dados relacional.

## 4. Escopo do sistema

### 4.1 Funcionalidades incluídas

- Login e encerramento de sessão.
- Painel do professor com listagem de atividades publicadas.
- Cadastro de atividade com título, descrição e data de entrega opcional.
- Painel do aluno com atividades e situação da entrega.
- Envio e edição de resposta textual.
- Visualização das entregas pelo professor.
- Registro e atualização de nota e feedback.

### 4.2 Limitações e itens fora do escopo

- Não há envio de anexos ou arquivos; a resposta é textual.
- Não há cadastro público de usuários; o protótipo inicia com duas contas demonstrativas.
- Não há notificações por e-mail, chat, videoconferência ou integração com plataformas externas.
- Não há relatórios avançados, inteligência artificial ou aplicativo móvel nativo.
- O protótipo foi preparado para execução local e não deve ser publicado em produção sem reforços de segurança.

## 5. Requisitos do sistema

### 5.1 Requisitos funcionais

| Código | Descrição |
|---|---|
| RF01 | O sistema deve permitir que um usuário autenticado acesse o painel correspondente ao seu perfil. |
| RF02 | O sistema deve permitir que o professor publique uma atividade com título e descrição. |
| RF03 | O sistema deve permitir a inclusão opcional de data de entrega. |
| RF04 | O sistema deve listar para o aluno as atividades publicadas. |
| RF05 | O sistema deve permitir que o aluno envie e atualize uma resposta textual. |
| RF06 | O sistema deve permitir que o professor consulte as respostas de suas atividades. |
| RF07 | O sistema deve permitir que o professor registre uma nota entre zero e dez e um feedback textual. |
| RF08 | O sistema deve permitir que o usuário encerre sua sessão. |

### 5.2 Requisitos não funcionais

- **RNF01:** A aplicação deve ser acessível por navegador WEB atualizado.
- **RNF02:** A interface deve se adaptar a telas de computadores e dispositivos móveis.
- **RNF03:** As senhas devem ser armazenadas como hashes, e não em texto puro.
- **RNF04:** As rotas devem verificar a autenticação e o perfil antes de liberar operações restritas.
- **RNF05:** Os dados devem permanecer armazenados após o encerramento da aplicação.
- **RNF06:** O código deve ser organizado de forma que permita manutenção e evolução.

## 6. Fundamentação teórica e tecnologias

### 6.1 Aplicações WEB

Uma aplicação WEB utiliza protocolos e tecnologias da WEB para disponibilizar recursos por meio de um navegador. Em uma arquitetura cliente-servidor, o navegador apresenta a interface e envia requisições ao servidor, que processa as regras da aplicação e acessa os dados necessários. Essa separação permite organizar a apresentação, o processamento e a persistência.

### 6.2 Python e Flask

Python é uma linguagem de programação de alto nível, utilizada em diferentes áreas do desenvolvimento de software (PYTHON SOFTWARE FOUNDATION, s.d.). Flask é um microframework WEB para Python que fornece recursos para definição de rotas, tratamento de requisições e renderização de páginas (PALLETS PROJECTS, s.d.). Sua estrutura enxuta é adequada a aplicações pequenas e protótipos acadêmicos.

### 6.3 HTML, CSS e JavaScript

HTML define a estrutura e o significado do conteúdo apresentado no navegador. CSS controla a apresentação visual e a adaptação do layout a diferentes tamanhos de tela. JavaScript permite adicionar comportamento no lado do cliente (MDN WEB DOCS, s.d.). Nesta versão, a maior parte das operações é processada no servidor, enquanto HTML e CSS formam a interface principal.

### 6.4 SQLite

SQLite é um mecanismo de banco de dados relacional que armazena os dados em um arquivo local, dispensando a instalação e administração de um servidor de banco separado (SQLITE, s.d.). Foi escolhido para simplificar a instalação e a demonstração do protótipo.

### 6.5 Segurança básica

O sistema utiliza hash de senha por meio das ferramentas de segurança do Werkzeug, sessões para identificar usuários autenticados e verificações de perfil nas rotas restritas. Essas medidas representam uma base didática, mas não substituem uma revisão de segurança para implantação pública. Antes de produção, devem ser adicionados, entre outros controles, proteção CSRF, HTTPS, gestão segura de segredos, limitação de tentativas e configuração adequada de cookies.

## 7. Arquitetura e funcionamento

A aplicação segue uma organização cliente-servidor. O navegador solicita páginas e envia formulários HTTP ao servidor Flask. As rotas validam a sessão e o perfil do usuário, executam as regras de negócio e consultam ou atualizam o banco SQLite. O servidor devolve páginas HTML renderizadas com os dados correspondentes.

- **Camada de apresentação:** arquivos HTML em `templates/` e estilos em `static/style.css`.
- **Camada de aplicação:** rotas, autenticação, autorização e regras de negócio em `app.py`.
- **Camada de dados:** tabelas relacionais armazenadas em `lumia.db`.

## 8. Modelagem de dados

O banco de dados possui três entidades principais:

- **users:** armazena identificador, nome, e-mail único, hash da senha e perfil (`teacher` ou `student`).
- **activities:** armazena título, descrição, data de entrega opcional e referência ao professor responsável.
- **submissions:** armazena a resposta textual, aluno, atividade, data de envio, nota e feedback. A combinação atividade/aluno é única, permitindo atualizar uma entrega sem criar duplicatas.

Relacionamentos: um professor pode cadastrar várias atividades; uma atividade pode receber várias entregas; um aluno pode realizar entregas em várias atividades. Cada entrega pertence a um aluno e a uma atividade.

## 9. Implementação

A implementação está concentrada inicialmente no arquivo `app.py` para facilitar a leitura do protótipo. A inicialização cria as tabelas quando necessário e insere duas contas demonstrativas somente se a tabela de usuários estiver vazia.

O perfil `teacher` acessa o cadastro de atividades e a consulta das entregas das atividades sob sua responsabilidade. O perfil `student` acessa o painel de atividades, envia uma resposta textual e consulta a nota e o feedback quando registrados. As rotas de cada perfil são protegidas por verificações de autorização.

A interface foi dividida em modelos HTML reutilizáveis: base, login, painéis de professor e aluno, formulário de atividade, formulário de entrega, listagem de entregas e página de erro.

## 10. Plano de testes

Os testes abaixo constituem um roteiro de validação manual. Os resultados devem ser preenchidos pelo grupo após executar o sistema no ambiente de apresentação. Não se deve registrar como aprovado um teste que ainda não tenha sido realizado.

| Código | Procedimento | Resultado esperado | Resultado obtido |
|---|---|---|---|
| CT01 | Entrar com as credenciais válidas de professor | Painel do professor é exibido | A preencher |
| CT02 | Entrar com as credenciais válidas de aluno | Painel do aluno é exibido | A preencher |
| CT03 | Tentar login com senha incorreta | Mensagem de credenciais inválidas | A preencher |
| CT04 | Professor cadastrar atividade | Atividade aparece no painel | A preencher |
| CT05 | Aluno enviar resposta | Entrega aparece no painel do professor | A preencher |
| CT06 | Professor registrar nota e feedback | Aluno visualiza nota e feedback | A preencher |
| CT07 | Aluno tentar abrir rota exclusiva do professor | Acesso negado | A preencher |

## 11. Instalação e execução

1. Instalar Python 3.10 ou superior.
2. Abrir o terminal na pasta do projeto.
3. Criar e ativar um ambiente virtual (recomendado).
4. Executar `pip install -r requirements.txt`.
5. Executar `python app.py`.
6. Abrir `http://127.0.0.1:5000` no navegador.

**Contas demonstrativas:** `professor@lumia.com` e `aluno@lumia.com`. A senha inicial de ambas é `123456`. Essas credenciais são destinadas exclusivamente à demonstração local e devem ser alteradas ou removidas antes de qualquer implantação real.

## 12. Resultados esperados e considerações finais

Espera-se que o LumIA Web demonstre a construção de uma aplicação WEB integrada a um banco de dados, com autenticação, diferenciação de permissões e operações de cadastro, consulta e atualização. O escopo reduzido permite apresentar um fluxo completo: o professor publica uma atividade, o aluno envia uma resposta e o professor registra uma avaliação.

Como evolução futura, o projeto poderá receber cadastro administrativo de usuários, anexos, filtros, relatórios, notificações e uma interface de programação de aplicações (API). Essas funcionalidades não fazem parte da versão inicial e não são necessárias para demonstrar o fluxo central proposto.

## Referências

- FLASK. *Flask Documentation*. Disponível em: https://flask.palletsprojects.com/. Acesso em: 11 nov. 2026.
- PYTHON SOFTWARE FOUNDATION. *Python 3 Documentation*. Disponível em: https://docs.python.org/3/. Acesso em: 11 nov. 2026.
- SQLITE. *SQLite Documentation*. Disponível em: https://www.sqlite.org/docs.html. Acesso em: 11 nov. 2026.
- MDN WEB DOCS. *HTML: HyperText Markup Language*. Disponível em: https://developer.mozilla.org/docs/Web/HTML. Acesso em: 11 nov. 2026.
- MDN WEB DOCS. *CSS: Cascading Style Sheets*. Disponível em: https://developer.mozilla.org/docs/Web/CSS. Acesso em: 11 nov. 2026.

## Apêndice A – Estrutura dos arquivos

- `app.py`: aplicação Flask, rotas, autenticação e acesso ao banco.
- `requirements.txt`: dependências do projeto.
- `templates/`: páginas HTML.
- `static/style.css`: identidade visual e estilos responsivos.
- `lumia.db`: banco SQLite criado automaticamente na primeira execução.
- `README.md`: instruções resumidas de instalação e execução.

## Apêndice B – Cuidados antes da entrega

- Confirmar orientador e dados institucionais.
- Conferir o manual UNISA e ajustar a formatação.
- Executar os testes e registrar os resultados obtidos.
- Adicionar capturas reais das telas, caso solicitado.
- Antes da publicação de uma versão em produção, trocar a chave e desativar o modo de depuração.
