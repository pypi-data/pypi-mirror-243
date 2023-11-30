from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'', settings.ROOT_URLCONF, name='home'),
    host(r'stela.emmerut.com', 'stela_control.urls', name='stela'),

)