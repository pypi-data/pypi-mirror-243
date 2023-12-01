from django.contrib.sessions.models import Session

s = Session.objects.get(pk='2b1189a188b44ad18c35e113ac6ceead')
s.decoded()
