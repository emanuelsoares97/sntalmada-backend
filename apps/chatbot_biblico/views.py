
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import SessaoChat, MensagemChat
from .serializers import (
    ChatInputSerializer, 
    SessaoChatSerializer, 
    MensagemChatSerializer
)
from .services import PerplexityService
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
def chat_api(request):
    """
    Endpoint principal do chat bíblico.
    Aqui é onde o frontend manda as perguntas e recebe as respostas do bot.
    """
    dados = ChatInputSerializer(data=request.data)

    if not dados.is_valid():
        return Response(
            {'erro': 'Os dados que enviaste não estão válidos', 'detalhes': dados.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    pergunta = dados.validated_data['pergunta']
    sessao_id = dados.validated_data.get('sessao_id')

    try:
        # Se já existe sessão, vai buscar. Se não, cria uma nova.
        if sessao_id:
            sessao = get_object_or_404(SessaoChat, id=sessao_id, ativo=True)
        else:
            sessao = SessaoChat.objects.create()

        # Guarda a mensagem do utilizador
        msg_utilizador = MensagemChat.objects.create(
            sessao=sessao,
            tipo='utilizador',
            conteudo=pergunta,
            status='concluido'
        )

        # Chama o serviço da Perplexity para tratar a pergunta
        servico = PerplexityService()
        resultado = servico.processar_chat(pergunta)

        # Guarda a resposta do bot
        msg_bot = MensagemChat.objects.create(
            sessao=sessao,
            tipo='bot',
            conteudo=resultado['resposta'],
            e_biblico=resultado['e_biblico'],
            status=resultado['status']
        )

        # Dá um título à sessão se ainda não tiver
        if not sessao.titulo or sessao.titulo == "Nova Conversa":
            sessao.titulo = pergunta[:50] + "..." if len(pergunta) > 50 else pergunta
            sessao.save()

        return Response({
            'resposta': resultado['resposta'],
            'e_biblico': resultado['e_biblico'],
            'status': resultado['status'],
            'sessao_id': sessao.id,
            'mensagem_id': msg_bot.id
        })

    except Exception as e:
        logger.error(f"Erro no chat: {e}")
        return Response(
            {'erro': 'Erro interno, algo correu mal do nosso lado.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def listar_sessoes(request):
    """
    Lista as sessões de chat que ainda estão ativas.
    """
    sessoes = SessaoChat.objects.filter(ativo=True)[:20]
    dados = SessaoChatSerializer(sessoes, many=True)
    return Response({'sessoes': dados.data})


@api_view(['GET'])
def detalhes_sessao(request, sessao_id):
    """
    Vai buscar os detalhes de uma sessão específica.
    """
    sessao = get_object_or_404(SessaoChat, id=sessao_id, ativo=True)
    dados = SessaoChatSerializer(sessao)
    return Response(dados.data)


@api_view(['DELETE'])
def deletar_sessao(request, sessao_id):
    """
    Remove uma sessão de chat (fica inativa).
    """
    sessao = get_object_or_404(SessaoChat, id=sessao_id)
    sessao.ativo = False
    sessao.save()
    return Response({'mensagem': 'Sessão removida com sucesso'})