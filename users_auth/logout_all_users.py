from django.contrib.sessions.models import Session
close = Session.objects.all().delete()

close