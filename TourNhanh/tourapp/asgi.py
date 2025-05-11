"""
ASGI config for tourapp project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourapp.settings')

application = get_asgi_application()
