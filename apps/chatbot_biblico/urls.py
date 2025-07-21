
from django.urls import path
from .views import chat_api, listar_sessoes, detalhes_sessao, deletar_sessao

app_name = 'chatbot_biblico'

urlpatterns = [
    path('chat/', chat_api, name='chat_api'),  # Endpoint para enviar perguntas ao bot
    path('sessoes/', listar_sessoes, name='listar_sessoes'),  # Lista as sessões
    path('sessoes/<int:sessao_id>/', detalhes_sessao, name='detalhes_sessao'),  # Detalhes de uma sessão
    path('sessoes/<int:sessao_id>/deletar/', deletar_sessao, name='deletar_sessao'),  # Remove sessão
] 