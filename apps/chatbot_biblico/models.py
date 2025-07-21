from django.db import models

class SessaoChat(models.Model):
    titulo = models.CharField(max_length=200, default="Nova Conversa")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-atualizado_em']
        verbose_name = "Sessão de Chat"
        verbose_name_plural = "Sessões de Chat"

class MensagemChat(models.Model):
    TIPO_CHOICES = [
        ('usuario', 'Usuário'),
        ('assistente', 'Assistente'),
    ]
    
    STATUS_CHOICES = [
        ('processando', 'Processando'),
        ('concluido', 'Concluído'),
        ('rejeitado', 'Rejeitado'),
        ('erro', 'Erro'),
    ]
    
    sessao = models.ForeignKey(
        SessaoChat, 
        on_delete=models.CASCADE, 
        related_name='mensagens'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    conteudo = models.TextField()
    e_biblico = models.BooleanField(default=True)
    citacoes = models.JSONField(default=list, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='processando'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['criado_em']
        verbose_name = "Mensagem de Chat"
        verbose_name_plural = "Mensagens de Chat" 