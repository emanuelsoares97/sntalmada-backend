# SNT Almada - Backend

Este é o repositório backend para o site da SNT Almada, desenvolvido com Django e Django Rest Framework.

## Funcionalidades

- API para Chatbot Bíblico com IA (usando Perplexity AI).
- Gerenciamento de sessões e mensagens de chat.
- Estrutura de configurações separada para desenvolvimento e produção.
- Pronto para deploy em plataformas como Railway ou Render.

## Como começar

1. Clone o repositório.
2. Crie e ative um ambiente virtual: `python -m venv env` e `source env/bin/activate`.
3. Instale as dependências: `pip install -r requirements.txt`.
4. Crie um arquivo `.env` a partir do `.env.example` e preencha as variáveis.
5. Rode as migrações: `python manage.py migrate`.
6. Inicie o servidor de desenvolvimento: `python manage.py runserver`. 