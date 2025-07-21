# Configurações para o ambiente de teste
from .base import *

DEBUG = True

# Use um banco de dados em memória para testes rápidos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
} 