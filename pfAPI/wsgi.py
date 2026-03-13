"""
WSGI config for pfAPI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# uncomment for pythonanywhere
# path = "/home/delbrocco/comp3011-cswk-1"
# if path not in sys.path:
#     sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pfAPI.settings')

application = get_wsgi_application()
