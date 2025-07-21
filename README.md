
# SNT Almada - Backend

Backend do site da SNT Almada. Feito em Django + Django Rest Framework. Aqui está tudo o que precisas para meter o chat bíblico a funcionar.

## Instalação rápida

1. Faz clone do repositório.
2. Cria ambiente virtual:
   - `python -m venv env`
   - Ativa: `env\Scripts\activate` (Windows) ou `source env/bin/activate` (Linux/Mac)
3. Instala dependências:
   - `pip install -r requirements.txt`
4. Copia `.env.example` para `.env` e mete a tua chave Perplexity lá.
5. Faz as migrações:
   - `python manage.py migrate`
6. Corre o servidor:
   - `python manage.py runserver`

## Como funciona o chat

- Só responde perguntas sobre Bíblia, cristianismo ou teologia.
- Perguntas fora desse tema recebem resposta padrão.
- Se perguntares por pastores ou comunidade, responde também.
- As respostas não têm referências tipo [1], [2], etc.

## Estrutura

- apps/chatbot_biblico: lógica do chat, integra com Perplexity.
- sntalmada/settings: configurações para dev, produção, testing.
- manage.py: comando principal do Django.

## Ambiente de produção

- Pronto para deploy em Railway, Render, ou outro serviço que corra Django.
- Usa variáveis de ambiente para chave Perplexity e settings.

## Dicas

- Se nunca mexeste em Django, lê o código dos apps e das views para perceber como funciona.
- Qualquer dúvida, pergunta ou pede exemplos.

---
Projeto mantido por SNT Almada. Qualquer sugestão ou bug, avisa.
