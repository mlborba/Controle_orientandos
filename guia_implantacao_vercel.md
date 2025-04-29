# Guia de Implantação no Vercel

Este guia explica como implantar o Sistema de Controle de Orientandos permanentemente na plataforma Vercel.

## Pré-requisitos

1. Uma conta no [Vercel](https://vercel.com) (você pode se cadastrar gratuitamente)
2. Git instalado no seu computador (opcional, mas recomendado)

## Método 1: Implantação via GitHub

Este é o método mais simples e recomendado:

1. Crie um repositório no GitHub e faça upload dos arquivos do sistema
2. Faça login no Vercel com sua conta GitHub
3. Clique em "New Project" no dashboard do Vercel
4. Selecione o repositório que contém o sistema
5. Mantenha as configurações padrão (o arquivo vercel.json já contém todas as configurações necessárias)
6. Clique em "Deploy"

## Método 2: Implantação via CLI do Vercel

Se preferir usar a linha de comando:

1. Instale o Vercel CLI:
   ```
   npm install -g vercel
   ```

2. Faça login no Vercel:
   ```
   vercel login
   ```

3. Navegue até a pasta do projeto e execute:
   ```
   vercel
   ```

4. Siga as instruções na tela para completar a implantação

## Método 3: Upload direto pelo Dashboard

Se não quiser usar Git ou linha de comando:

1. Faça login no [Dashboard do Vercel](https://vercel.com/dashboard)
2. Clique em "New Project" e depois em "Upload"
3. Arraste e solte a pasta do projeto ou selecione os arquivos
4. Clique em "Deploy"

## Configurações Adicionais

### Domínio Personalizado

1. Após a implantação, vá para as configurações do projeto no Dashboard do Vercel
2. Clique em "Domains"
3. Adicione seu domínio personalizado e siga as instruções

### Variáveis de Ambiente

Se necessário, configure variáveis de ambiente no Dashboard do Vercel:

1. Vá para as configurações do projeto
2. Clique em "Environment Variables"
3. Adicione as variáveis necessárias (ex: SECRET_KEY)

## Primeiro Acesso

Após a implantação, acesse o sistema com as credenciais padrão:
- Usuário: `admin`
- Senha: `admin123`

**Importante**: Altere a senha do administrador após o primeiro acesso.

## Suporte

Se encontrar algum problema durante a implantação, consulte a [documentação oficial do Vercel](https://vercel.com/docs) ou entre em contato com o desenvolvedor.
