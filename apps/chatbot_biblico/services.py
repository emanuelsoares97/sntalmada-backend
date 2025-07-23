import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class PerplexityService:
    def __init__(self):
        self.api_key = settings.PERPLEXITY_API_KEY
        self.base_url = "https://api.perplexity.ai/chat/completions"
    
    def detectar_saudacao(self, pergunta):
        import re
        saudacoes = [
            'olá', 'ola', 'oi', 'bom dia', 'boa tarde', 'boa noite', 'tudo bem', 'como vai', 'paz', 'paz do senhor'
        ]
        pergunta_lower = pergunta.lower()
        # Verifica se alguma saudação aparece como palavra inteira ou frase
        for saudacao in saudacoes:
            # Usa regex para garantir que é palavra/frase isolada
            padrao = r'\b' + re.escape(saudacao) + r'\b'
            if re.search(padrao, pergunta_lower):
                return True
        return False
    
    def verificar_pergunta_biblica(self, pergunta):
        """Verifica se é pergunta bíblica usando modelo econômico"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = (
            f'A seguinte pergunta é sobre Bíblia, cristianismo ou teologia? "{pergunta}" '
            'Responda apenas com SIM ou NÃO, sem explicações.'
        )
        
        payload = {
            "model": "sonar",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 10,
            "temperature": 0.1
        }
        
        try:
            response = requests.post(
                self.base_url, 
                headers=headers, 
                json=payload, 
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            answer = result['choices'][0]['message']['content'].strip().upper()
            logger.info(f"Resposta da verificação bíblica: {answer}")
            if answer.startswith('SIM'):
                return True
            if answer.startswith('NÃO'):
                return False
            # fallback para palavras-chave óbvias
            if any(p in pergunta.lower() for p in [
                'jesus', 'deus', 'bíblia', 'apóstolo', 'evangelho', 'cristianismo',
                'discípulo', 'profeta', 'salmo', 'versículo', 'testamento', 'gênesis',
                'êxodo', 'apocalipse', 'milagre', 'pecado', 'ressurreição', 'cruz', 'igreja'
            ]):
                return True
            return False
            
        except Exception as e:
            logger.error(f"Erro na verificação bíblica: {e}")
            return False
    
    def responder_pergunta_biblica(self, pergunta):
        """Responde pergunta bíblica usando modelo básico"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = (
            "És um assistente virtual especializado em Bíblia, cristianismo e teologia evangélica. Todas as respostas devem seguir os princípios, ensinamentos e visão da Sara Nossa Terra – SNT Europa, respeitando os valores da tradição evangélica protestante. Privilegia sempre a interpretação bíblica ensinada pela SNT Europa e a sua missão de “fazer de cada pessoa um cristão, de cada cristão um discípulo e de cada discípulo um líder”. Quando necessário, cita passagens bíblicas e, em caso de diferentes interpretações dentro da denominação, apresenta-as de forma clara e respeitosa."
        )
        
        payload = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": pergunta}
            ],
            "max_tokens": 600,
            "temperature": 0.3
        }
        
        try:
            response = requests.post(
                self.base_url, 
                headers=headers, 
                json=payload, 
                timeout=45
            )
            response.raise_for_status()
            
            result = response.json()
            import re
            resposta = result['choices'][0]['message']['content']
            # Remove padrões como [1], [2], [3], ...
            resposta = re.sub(r'\s*\[\d+\]', '', resposta)
            return resposta
            
        except Exception as e:
            if hasattr(e, 'response') and e.response is not None:
                try:
                    logger.error(f"Erro na resposta bíblica: {e} | Status: {e.response.status_code} | Conteúdo: {e.response.text}")
                except Exception:
                    logger.error(f"Erro na resposta bíblica: {e} | Não foi possível obter detalhes da resposta.")
            else:
                logger.error(f"Erro na resposta bíblica: {e}")
            return "Desculpe, ocorreu um erro. Tente novamente."
    
    def processar_chat(self, pergunta):
        """Processa pergunta completa do chat, só responde perguntas bíblicas/cristãs/teologia"""
        # Responde saudações de forma especial
        if self.detectar_saudacao(pergunta):
            return {
                'resposta': 'Olá, família! Paz do Senhor! Como posso ajudar com a tua dúvida bíblica hoje?',
                'e_biblico': False,
                'status': 'saudacao'
            }

        # Só responde perguntas bíblicas/cristãs/teologia
        if not self.verificar_pergunta_biblica(pergunta):
            return {
                'resposta': 'Desculpa, só respondo perguntas sobre a Bíblia, cristianismo ou teologia. Se quiseres saber sobre a comunidade ou os pastores, pergunta diretamente a eles!',
                'e_biblico': False,
                'status': 'rejeitado'
            }

        resposta = self.responder_pergunta_biblica(pergunta)

        return {
            'resposta': resposta,
            'e_biblico': True,
            'status': 'concluido'
        }