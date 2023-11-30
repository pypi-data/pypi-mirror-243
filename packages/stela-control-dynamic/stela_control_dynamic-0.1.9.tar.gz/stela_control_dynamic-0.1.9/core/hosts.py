from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'', settings.ROOT_URLCONF, name='home'),
    host(r'stela.localhost:8000', 'stela_control.urls', name='stela'),

)