from rest_framework import serializers
from .models import SessaoChat, MensagemChat

class MensagemChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensagemChat
        fields = [
            'id', 'tipo', 'conteudo', 'e_biblico', 
            'citacoes', 'status', 'criado_em'
        ]
        read_only_fields = ['id', 'criado_em']

class SessaoChatSerializer(serializers.ModelSerializer):
    mensagens = MensagemChatSerializer(many=True, read_only=True)
    total_mensagens = serializers.SerializerMethodField()

    class Meta:
        model = SessaoChat
        fields = [
            'id', 'titulo', 'criado_em', 'atualizado_em', 
            'ativo', 'mensagens', 'total_mensagens'
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']

    def get_total_mensagens(self, obj):
        # Conta só as mensagens que estão concluídas
        return obj.mensagens.filter(status='concluido').count()

class ChatInputSerializer(serializers.Serializer):
    pergunta = serializers.CharField(max_length=500, trim_whitespace=True)
    sessao_id = serializers.IntegerField(required=False, allow_null=True)