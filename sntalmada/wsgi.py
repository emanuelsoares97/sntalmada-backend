import os
from django.core.wsgi import get_wsgi_application

settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'sntalmada.settings.development')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
 
application = get_wsgi_application() 