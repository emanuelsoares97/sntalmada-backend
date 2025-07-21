from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        'mensagem': 'API SNT Almada - Backend',
        'versao': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'chat_biblico': '/api/v1/chatbot/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root, name='api_root'),
    path('api/v1/chatbot/', include('apps.chatbot_biblico.urls')),
] 