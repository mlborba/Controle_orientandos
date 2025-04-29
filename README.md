# Sistema de Controle de Orientandos - Guia de Implantação

Este documento contém instruções para implantar o Sistema de Controle de Orientandos em um ambiente de produção.

## Conteúdo do Pacote

Este pacote contém uma aplicação web completa desenvolvida com Flask para gerenciar orientandos de mestrado, incluindo:

- Backend em Python/Flask com SQLite
- Interface responsiva com Bootstrap
- Funcionalidades de gerenciamento de orientandos, marcos, orientações e diário de orientação

## Requisitos

- Python 3.6 ou superior
- Pip (gerenciador de pacotes Python)
- Acesso a um serviço de hospedagem que suporte aplicações Python/Flask

## Opções de Implantação

### Opção 1: Heroku

1. Crie uma conta no [Heroku](https://www.heroku.com/) se ainda não tiver uma
2. Instale o [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. Faça login no Heroku CLI: `heroku login`
4. Crie um novo aplicativo Heroku: `heroku create nome-do-seu-app`
5. Inicialize um repositório Git na pasta do projeto:
   ```
   git init
   git add .
   git commit -m "Versão inicial"
   ```
6. Adicione o remote do Heroku: `heroku git:remote -a nome-do-seu-app`
7. Envie o código para o Heroku: `git push heroku master`
8. Abra o aplicativo: `heroku open`

### Opção 2: PythonAnywhere

1. Crie uma conta no [PythonAnywhere](https://www.pythonanywhere.com/)
2. Faça upload dos arquivos do projeto
3. Crie um novo aplicativo web:
   - Escolha Flask como framework
   - Configure o caminho para o arquivo WSGI
   - Aponte para o arquivo wsgi.py
4. Configure as variáveis de ambiente necessárias
5. Reinicie o aplicativo web

### Opção 3: Servidor VPS (Digital Ocean, AWS, etc.)

1. Configure um servidor com Ubuntu ou outra distribuição Linux
2. Instale Python e as dependências necessárias:
   ```
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```
3. Crie e ative um ambiente virtual:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
5. Configure um servidor WSGI como Gunicorn:
   ```
   pip install gunicorn
   gunicorn wsgi:app
   ```
6. Configure Nginx como proxy reverso (recomendado para produção)

## Configuração

### Variáveis de Ambiente

O aplicativo suporta as seguintes variáveis de ambiente:

- `SECRET_KEY`: Chave secreta para segurança da aplicação
- `DATABASE_URL`: URL de conexão com o banco de dados (padrão: SQLite local)
- `PORT`: Porta em que o aplicativo será executado (padrão: 5000)

### Banco de Dados

Por padrão, o aplicativo usa SQLite, que é adequado para implantações pequenas. Para implantações maiores, considere migrar para PostgreSQL ou MySQL.

## Primeiro Acesso

Após a implantação, acesse o sistema com as credenciais padrão:

- Usuário: `admin`
- Senha: `admin123`

**Importante**: Altere a senha do administrador após o primeiro acesso.

## Suporte

Para dúvidas ou problemas com a implantação, entre em contato com o desenvolvedor.

---

© 2025 Sistema de Controle de Orientandos
